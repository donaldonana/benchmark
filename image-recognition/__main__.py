from PIL import Image
import torch # type: ignore
from torchvision import transforms # type: ignore
from torchvision.models import resnet50, resnet18, resnet152, resnet34 # type: ignore
import datetime, json, os
import swiftclient

def recognition(event):

    # Swift identifiant
    auth_url = f'http://{event["ipv4"]}:8080/auth/v1.0'
    username = 'test:tester'
    password = 'testing'

    # Connect to Swift
    conn = swiftclient.Connection(
    	authurl=auth_url,
    	user=username,
    	key=password,
    	auth_version='1'
	)
    container = 'whiskcontainer'

    # Image Downloading
    image_download_begin = datetime.datetime.now()
    obj = conn.get_object(container, event["image"])
    with open(event["image"], 'wb') as f:
        f.write(obj[1])
    image_download_end = datetime.datetime.now()
    
    # Load class index file
    class_idx = json.load(open(os.path.join("/app", "imagenet_class_index.json"), 'r'))
    idx2label = [class_idx[str(e)][1] for e in range(len(class_idx))]
    model_path = os.path.join("/app", event["resnet"]+'.pth')
    
    # Load the resnet model
    model_load_begin = datetime.datetime.now()
    model = ResnetModel[event["resnet"]](pretrained=False)
    model.load_state_dict(torch.load(model_path))
    model.eval()
    model_load_end = datetime.datetime.now()
    model_size = os.path.getsize(model_path)
    
    # Begin image prediction
    prediction_begin = datetime.datetime.now()
    input_image = Image.open(event["image"]).convert('RGB')
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    input_tensor = preprocess(input_image)
    input_batch = input_tensor.unsqueeze(0)  
    output = model(input_batch)
    prob = torch.nn.functional.softmax(output[0], dim=0)  
    max_prob, max_prob_index = torch.max(prob, dim=0)
    label = idx2label[max_prob_index]
    prediction_end = datetime.datetime.now()

    # Times compute
    download_time   = (image_download_end - image_download_begin) / datetime.timedelta(seconds=1)
    model_load_time = (model_load_end - model_load_begin) / datetime.timedelta(seconds=1)
    prediction_time = (prediction_end - prediction_begin) / datetime.timedelta(seconds=1)
    
    return {
            'label': label, 
            'prob' : max_prob.item(),
            'index': max_prob_index.item(),
            'model_load_time': model_load_time,
            'prediction_time': prediction_time ,
            'download_time' : download_time,
            'image' : event["image"],
            'model' : event["resnet"],
            'model_size' : model_size
            }
             
ResnetModel = {'resnet18':resnet18, 'resnet34':resnet34, 'resnet50':resnet50, 'resnet152':resnet152}
    
def main(args):

    result = recognition({
        "image"  : args.get("image", '500b.JPEG'),
        "resnet" : args.get("resnet", "resnet18"),
        "ipv4"   : "10.245.158.103",
    })
     
    return result