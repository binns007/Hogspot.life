from fastapi import status, HTTPException,Depends, APIRouter,UploadFile, File, Form
from typing import List
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app import models, schemas, utils
from app.database import get_db
import random
from app.oauth2 import get_current_user
import boto3
from botocore.exceptions import NoCredentialsError
from app.config import settings
import logging
from sqlalchemy import func
import uuid


AWS_SERVER_PUBLIC_KEY = settings.AWS_SERVER_PUBLIC_KEY
AWS_SERVER_SECRET_KEY = settings.AWS_SERVER_SECRET_KEY

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    if user.password != user.confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match")

    hashed_password = utils.hash(user.password)
    new_user = models.User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        date_of_birth=user.date_of_birth
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@router.put("/complete_profile", response_model=schemas.UserOut)
def complete_profile(
    profile_data: schemas.CompleteProfile,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if profile_data.bio is not None:
        user.bio = profile_data.bio
    if profile_data.gender is not None:
        user.gender = profile_data.gender

    db.commit()
    db.refresh(user)
    
    return user

def upload_image_to_s3(image, bucket_name):
    s3 = boto3.client('s3', aws_access_key_id=AWS_SERVER_PUBLIC_KEY, aws_secret_access_key=AWS_SERVER_SECRET_KEY)
    try:
        unique_filename = f"{uuid.uuid4().hex}_{image.filename}"
        s3.upload_fileobj(image.file, bucket_name, unique_filename)
        image_url = f"https://{bucket_name}.s3.amazonaws.com/{unique_filename}"
        return image_url
    except NoCredentialsError:
        logging.error("Credentials not available")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="S3 credentials not available")
    except Exception as e:
        logging.error(f"Error uploading image: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error uploading image")

def parse_priorities(priorities_str: str) -> List[int]:
    try:
        return list(map(int, priorities_str.split(',')))
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Priorities must be a comma-separated list of integers")

@router.post("/upload_images", response_model=List[schemas.UserImageOut])
def upload_images(
    files: List[UploadFile] = File(...),
    current_user: models.User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    
    uploaded_images = []
    max_priority = db.query(func.max(models.UserImage.priority)).filter(models.UserImage.user_id == current_user.id).scalar() or 0
    for i, file in enumerate(files):
        file_url = upload_image_to_s3(file, 'hogspot')

        user_image = models.UserImage(
            user_id=user.id,
            image_url=file_url,
            priority=max_priority+1+i
        )
        db.add(user_image)
        db.commit()
        db.refresh(user_image)
        uploaded_images.append(user_image)

    return uploaded_images


@router.put("/update_image_priority/{image_id}", response_model=schemas.UserImageOut)
def update_image_priority(
    image_id: int,
    priority: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_image = db.query(models.UserImage).filter(models.UserImage.id == image_id, models.UserImage.user_id == current_user.id).first()
    if not user_image:
        raise HTTPException(status_code=404, detail="Image not found or not authorized")

    user_image.priority = priority
    db.commit()
    db.refresh(user_image)

    return user_image

@router.get("/profile_images", response_model=List[schemas.UserImageOut])
def get_profile_images(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    images = db.query(models.UserImage).filter(models.UserImage.user_id == current_user.id).order_by(models.UserImage.priority).all()
    return images