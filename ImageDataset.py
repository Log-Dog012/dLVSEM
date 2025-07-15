import os
import pandas as pd
from torch.utils.data import Dataset
from torchvision.io import decode_image

class ImageDataset(Dataset):
    def __init__(self, annotations_file, img_dir, transform=None, target_transform=None):
        self.img_labels = pd.read_csv(annotations_file)
        self.img_dir = img_dir
        self.transform = transform
        self.target_transform = target_transform

    def __len__(self):
        return len(self.img_labels)

    def __getitem__(self, idx):
        img_path = os.path.join(self.img_dir, self.img_labels.iat[idx, 1])
        image = decode_image(img_path)
        label = self.img_labels.iat[idx, 2]
        if self.transform:
            image = self.transform(image)
        if self.target_transform:
            label = self.target_transform(label)
        return image, label
    
if __name__=='__main__':
    mydataset=ImageDataset('Test/annotation.csv','Test')
    import matplotlib.pyplot as plt
    img,lab=mydataset[0]
    img = img.permute(1, 2, 0)
    plt.imshow(img)
    plt.title(lab)
    plt.show()
