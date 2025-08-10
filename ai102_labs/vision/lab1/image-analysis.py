from dotenv import load_dotenv
import os
from PIL import Image, ImageDraw
import sys
from matplotlib import pyplot as plt
from azure.core.exceptions import HttpResponseError
import requests

# import namespaces
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

from common.auth.credential_loader import AzureEnvLoader
env_loader = AzureEnvLoader()

script_dir = os.path.dirname(os.path.abspath(__file__))

def main():

    # Clear the console
    os.system('cls' if os.name=='nt' else 'clear')

    try:
        # Get Configuration Settings
        ai_endpoint = env_loader.get_variable('VISION_AZURE_AI_SERVICE_ENDPOINT')
        ai_key = env_loader.get_variable('VISION_AZURE_AI_SERVICE_KEY')

        # Get image
        image_file = os.path.join(script_dir, 'images', 'street.jpg')
        if len(sys.argv) > 1:
            image_file = sys.argv[1]
        

        # Authenticate Azure AI Vision client
        cv_client = ImageAnalysisClient(
            endpoint=ai_endpoint,
            credential=AzureKeyCredential(ai_key))

        # Analyze image
        with open(image_file, "rb") as f:
            image_data = f.read()
        print(f'\nAnalyzing {image_file}\n')

        result = cv_client.analyze(
            image_data=image_data,
            visual_features=[
                # VisualFeatures.CAPTION,
                # VisualFeatures.DENSE_CAPTIONS,
                VisualFeatures.TAGS,
                VisualFeatures.OBJECTS,
                VisualFeatures.PEOPLE],
        )
        print("Analysis complete.\n", result)

        # Get image captions
        if result.caption is not None:
            print("\nCaption:")
            print(" Caption: '{}' (confidence: {:.2f}%)".format(result.caption.text, result.caption.confidence * 100))
            
        if result.dense_captions is not None:
            print("\nDense Captions:")
            for caption in result.dense_captions.list:
                print(" Caption: '{}' (confidence: {:.2f}%)".format(caption.text, caption.confidence * 100))        

        # Get image tags
        if result.tags is not None:
            print("\nTags:")
            for tag in result.tags.list:
                print(" Tag: '{}' (confidence: {:.2f}%)".format(tag.name, tag.confidence * 100))

        # Get objects in the image
        if result.objects is not None:
            print("\nObjects in image:")
            for detected_object in result.objects.list:
                # Print object tag and confidence
                print(" {} (confidence: {:.2f}%)".format(detected_object.tags[0].name, detected_object.tags[0].confidence * 100))
            # Annotate objects in the image
            show_objects(image_file, result.objects.list)

        # Get people in the image
        if result.people is not None:
            print("\nPeople in image:")

            for detected_person in result.people.list:
                if detected_person.confidence > 0.2:
                    # Print location and confidence of each person detected
                    print(" {} (confidence: {:.2f}%)".format(detected_person.bounding_box, detected_person.confidence * 100))
            # Annotate people in the image
            show_people(image_file, result.people.list)

    except Exception as ex:
        print(ex)


def show_objects(image_filename, detected_objects):
    print ("\nAnnotating objects...")

    # Prepare image for drawing
    image = Image.open(image_filename)
    fig = plt.figure(figsize=(image.width/100, image.height/100))
    plt.axis('off')
    draw = ImageDraw.Draw(image)
    color = 'cyan'

    for detected_object in detected_objects:
        # Draw object bounding box
        r = detected_object.bounding_box
        bounding_box = ((r.x, r.y), (r.x + r.width, r.y + r.height)) 
        draw.rectangle(bounding_box, outline=color, width=3)
        plt.annotate(detected_object.tags[0].name,(r.x, r.y), backgroundcolor=color)

    # Save annotated image
    plt.imshow(image)
    plt.tight_layout(pad=0)
    objectfile = os.path.join(script_dir, 'images', 'objects.jpg')
    fig.savefig(objectfile)
    print('  Results saved in', objectfile)


def show_people(image_filename, detected_people):
    print ("\nAnnotating objects...")

    # Prepare image for drawing
    image = Image.open(image_filename)
    fig = plt.figure(figsize=(image.width/100, image.height/100))
    plt.axis('off')
    draw = ImageDraw.Draw(image)
    color = 'cyan'

    for detected_person in detected_people:
        if detected_person.confidence > 0.2:
            # Draw object bounding box
            r = detected_person.bounding_box
            bounding_box = ((r.x, r.y), (r.x + r.width, r.y + r.height))
            draw.rectangle(bounding_box, outline=color, width=3)

    # Save annotated image
    plt.imshow(image)
    plt.tight_layout(pad=0)
    peoplefile = os.path.join(script_dir, 'images', 'people.jpg')
    fig.savefig(peoplefile)
    print('  Results saved in', peoplefile)


if __name__ == "__main__":
    main()
