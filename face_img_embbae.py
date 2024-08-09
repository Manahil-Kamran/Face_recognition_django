import os
import gc
import psutil
import random
import numpy as np
import cv2
from PIL import Image
import torch
from utils.base import Resnet50
from utils.transform import make_transform

import warnings
warnings.filterwarnings("ignore")


seed = 1
random.seed(seed)
np.random.seed(seed)
torch.manual_seed(seed)
torch.cuda.manual_seed_all(seed) 


process = psutil.Process(os.getpid())
print(f"Before torch.load: {process.memory_info().rss / 1e6:.2f} MB")

model = Resnet50(embedding_size=512)  

checkpoint = torch.load("model/FR.pth", map_location=torch.device("cuda:0"))
model.load_state_dict(checkpoint['model_state_dict'])
model.eval() 
model.to(torch.device("cuda:0"))  
gc.collect()
print(f"After torch.load: {process.memory_info().rss / 1e6:.2f} MB")

image_path = '/home/zohaib-durrani/tr/cropedfaces/1901/389_.jpg'

image = cv2.imread(image_path)

image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

image = Image.fromarray(image)

transform = make_transform()

image = transform(image)

image = image.unsqueeze(0)
image = image.to(torch.device("cuda:0"))

with torch.no_grad():
    output = model(image)

output = output.cpu().numpy()

# print(len(output[0]))
print(np.array(output).tolist())
