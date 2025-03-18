import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from app.models.database import SessionLocal, save_to_db  

def get_all_images(collection_url):
    """
    Scrapes FirstView and collects all images for later filtering, along with collection details.
    """
    # Set up Chrome WebDriver
    options = Options()
    options.headless = True  
    options.add_argument("--log-level=3")  # Reduce console spam
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Set up WebDriver
    service = Service("C:/WebDrivers/chromedriver.exe")  
    driver = webdriver.Chrome(service=service, options=options)

    # Open the collection page
    driver.get(collection_url)
    time.sleep(2)  # Let the page load

    image_urls = []  # Store all images
    collection_title = None 
    season = None  # 
    designer_name = None
    collection_type = None
    description = None
    gender = None
    
    max_same_image_repeats = 3  # Stop after seeing the same image 3 times
    same_image_count = 0
    previous_image_url = None

    try:
        # Scrape collection title
        collection_title_element = driver.find_element(By.CSS_SELECTOR, "span.pageTitle")
        collection_title = collection_title_element.text.strip() if collection_title_element else "Unknown Collection"
        parts = [part.strip() for part in collection_title.split(" - ")]

        designer_name = parts[0] if len(parts) > 0 else None
        collection_type = parts[1] if len(parts) > 1 else None
        description = parts[2] if len(parts) > 2 else None
        gender = parts[3] if len(parts) > 3 else None
        
        # Scrape season
        season_element = driver.find_element(By.CSS_SELECTOR, "span.season")
        season = season_element.text.strip() if season_element else "Unknown Season"
        
        print("Collection Title: {collection_title}")
        print("Season: {season}")
        print("Designer:", designer_name)
        print("Collection Type:", collection_type)
        print("Description:", description)
        print("Gender:", gender)

    except Exception as e:
        print(f"Error occurred while scraping collection details: {str(e)}")

    while True:
        try:
            # Find the current image
            image_element = driver.find_element(By.CSS_SELECTOR, "img[src^='/files/']")
            img_src = image_element.get_attribute("src")
            img_url = img_src if img_src.startswith("http") else "https://www.firstview.com" + img_src

            # Prevent infinite loop by stopping when same image appears too many times
            if previous_image_url == img_url:
                same_image_count += 1
                if same_image_count >= max_same_image_repeats:
                    print(f"⚠ Detected end of slideshow, stopping.")
                    break
            else:
                same_image_count = 0  # Reset counter if a new image appears

            # Store all images
            print(f"Saving image: {img_url}")
            image_urls.append(img_url)
            previous_image_url = img_url  # Update last image reference
            
            # Save image details to DB
            with SessionLocal() as db_session:
                save_to_db(db_session, img_url, designer_name, season, collection_type, description, gender)

            # Find and click the "Next" button
            try:
                next_button = driver.find_element(By.XPATH, "//a[contains(text(), 'next')]")
            except:
                next_button = driver.find_element(By.XPATH, "//a/img[contains(@src, 'next_n.gif')]/parent::a")

            driver.execute_script("arguments[0].click();", next_button)  # JavaScript click workaround
            time.sleep(.5)  # Small delay to let next image load

        except Exception as e:
            print("⚠ No more images or error occurred:", str(e))
            break  # Stop when no "Next" button is found

    driver.quit()  # Close browser session
    return image_urls

if __name__ == "__main__":
    """
    Change this URL for the desired runway collection.
    """
    COLLECTION_URL = "https://www.firstview.com/collection_image_closeup.php?of=0&collection=53877&image=8590537"

    print(f"Fetching images from: {COLLECTION_URL}\n")
    images = get_all_images(COLLECTION_URL)

    if images:
        print(f"\n Collected {len(images)} images for later filtering:")
        for img in images[:5]:  # Show first 5 images
            print(img)
    else:
        print("No images found.")

