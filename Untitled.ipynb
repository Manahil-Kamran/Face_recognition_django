{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "6e1da214-23fc-4978-9714-43335cfd130e",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "'/home/devp/Face_recognition_django'"
      ]
     },
     "execution_count": 1,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "pwd"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "3a4385ad-de68-4e12-bc51-e98fd4f62b2f",
   "metadata": {},
   "outputs": [],
   "source": [
    "import csv\n",
    "import os\n",
    "import gc\n",
    "import psutil\n",
    "import random\n",
    "import numpy as np\n",
    "import cv2\n",
    "from PIL import Image\n",
    "import torch\n",
    "from my_utils.base import Resnet50\n",
    "from my_utils.transform import make_transform\n",
    "from django.utils.timezone import now\n",
    "import warnings\n",
    "import psycopg2\n",
    "import os\n",
    "import pandas as pd  \n",
    "from sqlalchemy import create_engine\n",
    "from django.conf import settings\n",
    "from django.apps import apps\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "dda2072a-dc53-4c8c-b1f3-3d18d34fd32e",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Setup Django settings\n",
    "os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configurations.settings')\n",
    "import django\n",
    "django.setup()\n",
    "\n",
    "# Import your Django models\n",
    "PersonRegistration = apps.get_model('dashboard', 'PersonRegistration')\n",
    "FaceCoding = apps.get_model('dashboard', 'FaceCoding')\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "2888c73b-b98c-443c-91af-f8172110c928",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Before torch.load: 566.31 MB\n",
      "ResNetSSD caffe model loaded successfully\n",
      "After torch.load: 800.26 MB\n"
     ]
    }
   ],
   "source": [
    "warnings.filterwarnings(\"ignore\")\n",
    "\n",
    "# Set random seeds for reproducibility\n",
    "seed = 1\n",
    "random.seed(seed)\n",
    "np.random.seed(seed)\n",
    "torch.manual_seed(seed)\n",
    "torch.cuda.manual_seed_all(seed)\n",
    "\n",
    "# Monitor memory usage before loading the model\n",
    "process = psutil.Process(os.getpid())\n",
    "print(f\"Before torch.load: {process.memory_info().rss / 1e6:.2f} MB\")\n",
    "\n",
    "# Load the face detection model (ResNet SSD)\n",
    "prototxt_file = 'Resnet_SSD_deploy.prototxt'\n",
    "caffemodel_file = 'Res10_300x300_SSD_iter_140000.caffemodel'\n",
    "net = cv2.dnn.readNetFromCaffe(prototxt_file, caffemodel_file)\n",
    "print('ResNetSSD caffe model loaded successfully')\n",
    "\n",
    "# Load the ResNet50 model for face embedding extraction\n",
    "model = Resnet50(embedding_size=512)\n",
    "checkpoint = torch.load(\"/home/devp/Downloads/FR.pth\", map_location=torch.device(\"cpu\"))\n",
    "model.load_state_dict(checkpoint['model_state_dict'])\n",
    "model.eval()  # Set the model to evaluation mode\n",
    "model.to(torch.device(\"cpu\"))  # Move the model to CPU\n",
    "gc.collect()\n",
    "print(f\"After torch.load: {process.memory_info().rss / 1e6:.2f} MB\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "0cb6b51a-0ceb-409b-91cc-fa194f1f61d8",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Directory containing the dataset\n",
    "dataset_path = '/home/devp/dataset'\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "a8b5f9bd-6f24-4896-9a66-79e537eee6d0",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Processing image: /home/devp/dataset/87261/36209.jpg for employee ID: 87261\n"
     ]
    },
    {
     "ename": "SynchronousOnlyOperation",
     "evalue": "You cannot call this from an async context - use a thread or sync_to_async.",
     "output_type": "error",
     "traceback": [
      "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[0;31mSynchronousOnlyOperation\u001b[0m                  Traceback (most recent call last)",
      "Cell \u001b[0;32mIn[6], line 56\u001b[0m\n\u001b[1;32m     54\u001b[0m \u001b[38;5;66;03m# Fetch the person object (foreign key) from PersonRegistration\u001b[39;00m\n\u001b[1;32m     55\u001b[0m \u001b[38;5;28;01mtry\u001b[39;00m:\n\u001b[0;32m---> 56\u001b[0m     person \u001b[38;5;241m=\u001b[39m \u001b[43mPersonRegistration\u001b[49m\u001b[38;5;241;43m.\u001b[39;49m\u001b[43mobjects\u001b[49m\u001b[38;5;241;43m.\u001b[39;49m\u001b[43mget\u001b[49m\u001b[43m(\u001b[49m\u001b[38;5;28;43mid\u001b[39;49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43memployee_id\u001b[49m\u001b[43m)\u001b[49m\n\u001b[1;32m     57\u001b[0m \u001b[38;5;28;01mexcept\u001b[39;00m PersonRegistration\u001b[38;5;241m.\u001b[39mDoesNotExist:\n\u001b[1;32m     58\u001b[0m     \u001b[38;5;28mprint\u001b[39m(\u001b[38;5;124mf\u001b[39m\u001b[38;5;124m\"\u001b[39m\u001b[38;5;124mPerson with ID \u001b[39m\u001b[38;5;132;01m{\u001b[39;00memployee_id\u001b[38;5;132;01m}\u001b[39;00m\u001b[38;5;124m not found in PersonRegistration\u001b[39m\u001b[38;5;124m\"\u001b[39m)\n",
      "File \u001b[0;32m~/Face_recognition_django/envs/lib/python3.10/site-packages/django/db/models/manager.py:85\u001b[0m, in \u001b[0;36mBaseManager._get_queryset_methods.<locals>.create_method.<locals>.manager_method\u001b[0;34m(self, *args, **kwargs)\u001b[0m\n\u001b[1;32m     84\u001b[0m \u001b[38;5;28;01mdef\u001b[39;00m \u001b[38;5;21mmanager_method\u001b[39m(\u001b[38;5;28mself\u001b[39m, \u001b[38;5;241m*\u001b[39margs, \u001b[38;5;241m*\u001b[39m\u001b[38;5;241m*\u001b[39mkwargs):\n\u001b[0;32m---> 85\u001b[0m     \u001b[38;5;28;01mreturn\u001b[39;00m \u001b[38;5;28;43mgetattr\u001b[39;49m\u001b[43m(\u001b[49m\u001b[38;5;28;43mself\u001b[39;49m\u001b[38;5;241;43m.\u001b[39;49m\u001b[43mget_queryset\u001b[49m\u001b[43m(\u001b[49m\u001b[43m)\u001b[49m\u001b[43m,\u001b[49m\u001b[43m \u001b[49m\u001b[43mname\u001b[49m\u001b[43m)\u001b[49m\u001b[43m(\u001b[49m\u001b[38;5;241;43m*\u001b[39;49m\u001b[43margs\u001b[49m\u001b[43m,\u001b[49m\u001b[43m \u001b[49m\u001b[38;5;241;43m*\u001b[39;49m\u001b[38;5;241;43m*\u001b[39;49m\u001b[43mkwargs\u001b[49m\u001b[43m)\u001b[49m\n",
      "File \u001b[0;32m~/Face_recognition_django/envs/lib/python3.10/site-packages/django/db/models/query.py:646\u001b[0m, in \u001b[0;36mQuerySet.get\u001b[0;34m(self, *args, **kwargs)\u001b[0m\n\u001b[1;32m    644\u001b[0m     limit \u001b[38;5;241m=\u001b[39m MAX_GET_RESULTS\n\u001b[1;32m    645\u001b[0m     clone\u001b[38;5;241m.\u001b[39mquery\u001b[38;5;241m.\u001b[39mset_limits(high\u001b[38;5;241m=\u001b[39mlimit)\n\u001b[0;32m--> 646\u001b[0m num \u001b[38;5;241m=\u001b[39m \u001b[38;5;28;43mlen\u001b[39;49m\u001b[43m(\u001b[49m\u001b[43mclone\u001b[49m\u001b[43m)\u001b[49m\n\u001b[1;32m    647\u001b[0m \u001b[38;5;28;01mif\u001b[39;00m num \u001b[38;5;241m==\u001b[39m \u001b[38;5;241m1\u001b[39m:\n\u001b[1;32m    648\u001b[0m     \u001b[38;5;28;01mreturn\u001b[39;00m clone\u001b[38;5;241m.\u001b[39m_result_cache[\u001b[38;5;241m0\u001b[39m]\n",
      "File \u001b[0;32m~/Face_recognition_django/envs/lib/python3.10/site-packages/django/db/models/query.py:376\u001b[0m, in \u001b[0;36mQuerySet.__len__\u001b[0;34m(self)\u001b[0m\n\u001b[1;32m    375\u001b[0m \u001b[38;5;28;01mdef\u001b[39;00m \u001b[38;5;21m__len__\u001b[39m(\u001b[38;5;28mself\u001b[39m):\n\u001b[0;32m--> 376\u001b[0m     \u001b[38;5;28;43mself\u001b[39;49m\u001b[38;5;241;43m.\u001b[39;49m\u001b[43m_fetch_all\u001b[49m\u001b[43m(\u001b[49m\u001b[43m)\u001b[49m\n\u001b[1;32m    377\u001b[0m     \u001b[38;5;28;01mreturn\u001b[39;00m \u001b[38;5;28mlen\u001b[39m(\u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39m_result_cache)\n",
      "File \u001b[0;32m~/Face_recognition_django/envs/lib/python3.10/site-packages/django/db/models/query.py:1866\u001b[0m, in \u001b[0;36mQuerySet._fetch_all\u001b[0;34m(self)\u001b[0m\n\u001b[1;32m   1864\u001b[0m \u001b[38;5;28;01mdef\u001b[39;00m \u001b[38;5;21m_fetch_all\u001b[39m(\u001b[38;5;28mself\u001b[39m):\n\u001b[1;32m   1865\u001b[0m     \u001b[38;5;28;01mif\u001b[39;00m \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39m_result_cache \u001b[38;5;129;01mis\u001b[39;00m \u001b[38;5;28;01mNone\u001b[39;00m:\n\u001b[0;32m-> 1866\u001b[0m         \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39m_result_cache \u001b[38;5;241m=\u001b[39m \u001b[38;5;28;43mlist\u001b[39;49m\u001b[43m(\u001b[49m\u001b[38;5;28;43mself\u001b[39;49m\u001b[38;5;241;43m.\u001b[39;49m\u001b[43m_iterable_class\u001b[49m\u001b[43m(\u001b[49m\u001b[38;5;28;43mself\u001b[39;49m\u001b[43m)\u001b[49m\u001b[43m)\u001b[49m\n\u001b[1;32m   1867\u001b[0m     \u001b[38;5;28;01mif\u001b[39;00m \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39m_prefetch_related_lookups \u001b[38;5;129;01mand\u001b[39;00m \u001b[38;5;129;01mnot\u001b[39;00m \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39m_prefetch_done:\n\u001b[1;32m   1868\u001b[0m         \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39m_prefetch_related_objects()\n",
      "File \u001b[0;32m~/Face_recognition_django/envs/lib/python3.10/site-packages/django/db/models/query.py:87\u001b[0m, in \u001b[0;36mModelIterable.__iter__\u001b[0;34m(self)\u001b[0m\n\u001b[1;32m     84\u001b[0m compiler \u001b[38;5;241m=\u001b[39m queryset\u001b[38;5;241m.\u001b[39mquery\u001b[38;5;241m.\u001b[39mget_compiler(using\u001b[38;5;241m=\u001b[39mdb)\n\u001b[1;32m     85\u001b[0m \u001b[38;5;66;03m# Execute the query. This will also fill compiler.select, klass_info,\u001b[39;00m\n\u001b[1;32m     86\u001b[0m \u001b[38;5;66;03m# and annotations.\u001b[39;00m\n\u001b[0;32m---> 87\u001b[0m results \u001b[38;5;241m=\u001b[39m \u001b[43mcompiler\u001b[49m\u001b[38;5;241;43m.\u001b[39;49m\u001b[43mexecute_sql\u001b[49m\u001b[43m(\u001b[49m\n\u001b[1;32m     88\u001b[0m \u001b[43m    \u001b[49m\u001b[43mchunked_fetch\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[38;5;28;43mself\u001b[39;49m\u001b[38;5;241;43m.\u001b[39;49m\u001b[43mchunked_fetch\u001b[49m\u001b[43m,\u001b[49m\u001b[43m \u001b[49m\u001b[43mchunk_size\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[38;5;28;43mself\u001b[39;49m\u001b[38;5;241;43m.\u001b[39;49m\u001b[43mchunk_size\u001b[49m\n\u001b[1;32m     89\u001b[0m \u001b[43m\u001b[49m\u001b[43m)\u001b[49m\n\u001b[1;32m     90\u001b[0m select, klass_info, annotation_col_map \u001b[38;5;241m=\u001b[39m (\n\u001b[1;32m     91\u001b[0m     compiler\u001b[38;5;241m.\u001b[39mselect,\n\u001b[1;32m     92\u001b[0m     compiler\u001b[38;5;241m.\u001b[39mklass_info,\n\u001b[1;32m     93\u001b[0m     compiler\u001b[38;5;241m.\u001b[39mannotation_col_map,\n\u001b[1;32m     94\u001b[0m )\n\u001b[1;32m     95\u001b[0m model_cls \u001b[38;5;241m=\u001b[39m klass_info[\u001b[38;5;124m\"\u001b[39m\u001b[38;5;124mmodel\u001b[39m\u001b[38;5;124m\"\u001b[39m]\n",
      "File \u001b[0;32m~/Face_recognition_django/envs/lib/python3.10/site-packages/django/db/models/sql/compiler.py:1393\u001b[0m, in \u001b[0;36mSQLCompiler.execute_sql\u001b[0;34m(self, result_type, chunked_fetch, chunk_size)\u001b[0m\n\u001b[1;32m   1391\u001b[0m     cursor \u001b[38;5;241m=\u001b[39m \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39mconnection\u001b[38;5;241m.\u001b[39mchunked_cursor()\n\u001b[1;32m   1392\u001b[0m \u001b[38;5;28;01melse\u001b[39;00m:\n\u001b[0;32m-> 1393\u001b[0m     cursor \u001b[38;5;241m=\u001b[39m \u001b[38;5;28;43mself\u001b[39;49m\u001b[38;5;241;43m.\u001b[39;49m\u001b[43mconnection\u001b[49m\u001b[38;5;241;43m.\u001b[39;49m\u001b[43mcursor\u001b[49m\u001b[43m(\u001b[49m\u001b[43m)\u001b[49m\n\u001b[1;32m   1394\u001b[0m \u001b[38;5;28;01mtry\u001b[39;00m:\n\u001b[1;32m   1395\u001b[0m     cursor\u001b[38;5;241m.\u001b[39mexecute(sql, params)\n",
      "File \u001b[0;32m~/Face_recognition_django/envs/lib/python3.10/site-packages/django/utils/asyncio.py:24\u001b[0m, in \u001b[0;36masync_unsafe.<locals>.decorator.<locals>.inner\u001b[0;34m(*args, **kwargs)\u001b[0m\n\u001b[1;32m     22\u001b[0m \u001b[38;5;28;01melse\u001b[39;00m:\n\u001b[1;32m     23\u001b[0m     \u001b[38;5;28;01mif\u001b[39;00m \u001b[38;5;129;01mnot\u001b[39;00m os\u001b[38;5;241m.\u001b[39menviron\u001b[38;5;241m.\u001b[39mget(\u001b[38;5;124m\"\u001b[39m\u001b[38;5;124mDJANGO_ALLOW_ASYNC_UNSAFE\u001b[39m\u001b[38;5;124m\"\u001b[39m):\n\u001b[0;32m---> 24\u001b[0m         \u001b[38;5;28;01mraise\u001b[39;00m SynchronousOnlyOperation(message)\n\u001b[1;32m     25\u001b[0m \u001b[38;5;66;03m# Pass onward.\u001b[39;00m\n\u001b[1;32m     26\u001b[0m \u001b[38;5;28;01mreturn\u001b[39;00m func(\u001b[38;5;241m*\u001b[39margs, \u001b[38;5;241m*\u001b[39m\u001b[38;5;241m*\u001b[39mkwargs)\n",
      "\u001b[0;31mSynchronousOnlyOperation\u001b[0m: You cannot call this from an async context - use a thread or sync_to_async."
     ]
    }
   ],
   "source": [
    "# Loop through each employee folder in the dataset\n",
    "for employee_id in os.listdir(dataset_path):\n",
    "    employee_folder = os.path.join(dataset_path, employee_id)\n",
    "    \n",
    "    if not os.path.isdir(employee_folder):\n",
    "        continue  # Skip if it's not a directory\n",
    "\n",
    "    # Get list of image file paths for the employee\n",
    "    image_paths = [os.path.join(employee_folder, f) for f in os.listdir(employee_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]\n",
    "    \n",
    "    # Loop over each image for the current employee\n",
    "    for img_path in image_paths:\n",
    "        print(f\"Processing image: {img_path} for employee ID: {employee_id}\")\n",
    "        \n",
    "        # Load the image using OpenCV\n",
    "        image = cv2.imread(img_path)\n",
    "        if image is None:\n",
    "            print(f\"Failed to load image {img_path}\")\n",
    "            continue\n",
    "        (h, w) = image.shape[:2]\n",
    "\n",
    "        # Prepare the image for face detection\n",
    "        blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300), (104.0, 177.0, 123.0))\n",
    "        net.setInput(blob)\n",
    "        detections = net.forward()\n",
    "\n",
    "        # Loop over the detections\n",
    "        for i in range(detections.shape[2]):\n",
    "            confidence = detections[0, 0, i, 2]\n",
    "            \n",
    "            if confidence > 0.5:  # Filter out weak detections\n",
    "                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])\n",
    "                (startX, startY, endX, endY) = box.astype(\"int\")\n",
    "\n",
    "                # Extract the detected face ROI\n",
    "                face = image[startY:endY, startX:endX]\n",
    "\n",
    "                # Convert the face ROI to RGB and then to a PIL Image\n",
    "                face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)\n",
    "                face = Image.fromarray(face)\n",
    "\n",
    "                # Apply the necessary transformations to the face\n",
    "                transform = make_transform()\n",
    "                face = transform(face)\n",
    "\n",
    "                # Add a batch dimension and move the tensor to the CPU\n",
    "                face = face.unsqueeze(0)\n",
    "                face = face.to(torch.device(\"cpu\"))\n",
    "\n",
    "                # Perform face embedding extraction\n",
    "                with torch.no_grad():\n",
    "                    embedding = model(face).cpu().numpy().flatten()  # Flatten the embedding\n",
    "\n",
    "                # Fetch the person object (foreign key) from PersonRegistration\n",
    "                try:\n",
    "                    person = PersonRegistration.objects.get(id=employee_id)\n",
    "                except PersonRegistration.DoesNotExist:\n",
    "                    print(f\"Person with ID {employee_id} not found in PersonRegistration\")\n",
    "                    continue\n",
    "\n",
    "                # Save to FaceCoding model\n",
    "                face_coding = FaceCoding(\n",
    "                    person=person,  # Assign the foreign key person\n",
    "                    face_feature=embedding.tolist(),  # Store the face embedding\n",
    "                    img_url=img_path,  # Store the image URL\n",
    "                    date_created=now()  # Store current timestamp\n",
    "                )\n",
    "                face_coding.save()\n",
    "                print(f\"Saved embedding for employee ID: {employee_id} from image: {img_path}\")\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "8b67bd12-2de0-45a9-8723-89c6f9f5cff4",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.9"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
