import cv2
import dlib
import numpy as np
from sklearn.cluster import KMeans

# Load image
def load_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not load image at path: {image_path}")
    print("Original image shape and type:", image.shape, image.dtype)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

# Extract the dominant color using KMeans
def extract_dominant_color(region, k=3):
    pixels = region.reshape(-1, 3)
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(pixels)
    colors = kmeans.cluster_centers_
    labels, counts = np.unique(kmeans.labels_, return_counts=True)
    dominant = colors[labels[np.argmax(counts)]]
    return dominant.astype(int)

# 12-season classification based on color theory
def classify_season(r, g, b):
    if r > g and r > b:
        if r > 180 and g > 140:
            return "Light Spring" if b > 150 else "Warm Spring"
        elif g > 100:
            return "Warm Autumn" if b < 120 else "Soft Autumn"
        else:
            return "True Autumn"
    elif b > r and b > g:
        if b > 160 and r < 100:
            return "Light Summer" if g > 140 else "Soft Summer"
        elif r < 80:
            return "Cool Winter" if g > 100 else "Deep Winter"
        else:
            return "True Winter"
    else:
        return "Neutral" if r > 160 and g > 140 else "Soft Summer"

# Recommendations based on season
def get_color_recommendations(season):
    recommendations = {
        "True Winter": {
            "clothes": "Cool and intense colors, such as jewel tones (emerald, sapphire), black, and icy pastels.",
            "jewelry": "Silver, white gold, and cool-toned gemstones like sapphire and amethyst.",
            "makeup": "Cool, deep shades like berry or plum lipstick, and cool-toned eye shadows."
        },
        "Warm Spring": {
            "clothes": "Bright and warm colors like coral, turquoise, golden yellow, and peach.",
            "jewelry": "Gold and warm-toned gemstones like citrine or topaz.",
            "makeup": "Warm shades like coral lipstick, and golden eye shadows."
        },
        "Light Spring": {
            "clothes": "Soft and light colors like peach, mint green, pale yellow, and soft blue.",
            "jewelry": "Soft gold and pastel gemstones like aquamarine or light pink tourmaline.",
            "makeup": "Fresh shades like light pink lipstick and soft pastel eye shadows."
        },
        "True Autumn": {
            "clothes": "Rich, earthy colors like olive green, mustard yellow, rust, and brown.",
            "jewelry": "Gold and warm gemstones like amber, tiger’s eye, and carnelian.",
            "makeup": "Warm tones like brick red lipstick, and earthy eye shadows."
        },
        "Cool Winter": {
            "clothes": "Cool and crisp colors like icy blues, bright pinks, and contrasts with white or black.",
            "jewelry": "Silver and platinum with cool stones like topaz or diamond.",
            "makeup": "Crisp colors like bright pink lipstick and icy or silver-toned eyeshadows."
        },
        "Deep Winter": {
            "clothes": "Intense, dark, and cool colors like deep purples, burgundy, charcoal, and navy.",
            "jewelry": "Dark gemstones in silver or platinum settings, such as garnet or onyx.",
            "makeup": "Bold, dark lipstick shades like deep red, and smokey eye shadows in cool colors."
        },
        "Soft Autumn": {
            "clothes": "Muted, warm colors like camel, muted olive, and soft browns.",
            "jewelry": "Gold and warm stones like garnet or topaz.",
            "makeup": "Soft, warm makeup like peachy blush and soft brown lipstick."
        },
        "Soft Summer": {
            "clothes": "Muted colors like dusty rose, soft teal, lavender, and slate gray.",
            "jewelry": "Silver with soft-toned gemstones like moonstone or light jade.",
            "makeup": "Soft, natural tones like beige lipstick and gentle eye shadows."
        },
        "Light Summer": {
            "clothes": "Light, cool pastels like pale lavender, soft pink, and cool blues.",
            "jewelry": "Silver and cool-toned gemstones like amethyst or aquamarine.",
            "makeup": "Soft shades like rose lipstick and light, cool-toned eye shadows."
        },
        "Warm Autumn": {
            "clothes": "Rich, golden hues like camel, terracotta, and deep olive.",
            "jewelry": "Gold and warm stones like amber, ruby, or carnelian.",
            "makeup": "Warm lipstick shades like terracotta or brown, and deep golden eye shadows."
        },
        "True Winter": {
            "clothes": "Cool and deep colors like navy, black, and emerald.",
            "jewelry": "Silver and cool-toned stones like sapphire, ruby, or diamond.",
            "makeup": "Bold, rich colors like berry lipstick and deep, cool eyeshadow."
        },
    }
    return recommendations.get(season, {"clothes": "No recommendations available", "jewelry": "No recommendations available", "makeup": "No recommendations available"})

# Load dlib's face detector and landmark predictor
face_detector = dlib.get_frontal_face_detector()
landmark_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Detect facial features and extract color
def detect_features(image_path):
    image = load_image(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    
    faces = face_detector(gray)
    
    for face in faces:
        landmarks = landmark_predictor(gray, face)
        
        # Extract regions based on facial landmarks
        eye_region = image[landmarks.part(36).y:landmarks.part(39).y, landmarks.part(36).x:landmarks.part(39).x]
        hair_region = image[0:int(landmarks.part(27).y), :]  # Above eyebrows for hair
        skin_region = image[int(landmarks.part(29).y):int(landmarks.part(33).y), :]  # Cheek area

        eye_color = extract_dominant_color(eye_region)
        hair_color = extract_dominant_color(hair_region)
        skin_color = extract_dominant_color(skin_region)

        return eye_color, hair_color, skin_color

    return None, None, None

# Process image and classify based on automatic detection
def process_image_and_classify(image_path):
    eye_color, hair_color, skin_color = detect_features(image_path)
    
    if eye_color is None or hair_color is None or skin_color is None:
        return {"error": "Features not detected."}

    # Classify each feature into a season
    skin_season = classify_season(*skin_color)
    hair_season = classify_season(*hair_color)
    eye_season = classify_season(*eye_color)
    
    overall_season = skin_season  # Use the skin season as the dominant season
    recommendations = get_color_recommendations(overall_season)
    
    return {
        "season": overall_season,
        "recommendations": recommendations
    }