import pandas as pd
import os
import re
import unicodedata


# File paths
INPUT_FILE = os.path.join("assets", "alkon-hinnasto-tekstitiedostona.xlsx")
OUTPUT_FILE = os.path.join("data", "alko_generated_image_urls.xlsx")

# Ensure output directory exists
os.makedirs("data", exist_ok=True)

# Base URL
ALKO_IMAGE_BASE_URL = "https://images.alko.fi/images/cs_srgb,f_auto,t_medium/cdn/{numero}/{slug}.jpg"


def slugify(name: str) -> str:
    """
    Converts a product name into a URL-friendly slug for Alko image URLs.
    """
    # Normalize
    name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    # Lowercase
    name = name.lower()
    # Remove unwanted punctuation
    name = re.sub(r"[’'\".,!?:]", "", name)
    # Replace spaces and slashes with hyphens
    name = re.sub(r"[\s/]+", "-", name)
    # Collapse multiple hyphens
    name = re.sub(r"-+", "-", name)
    # Strip trailing hyphens
    name = name.strip("-")
    return name


def generate_image_url(numero: int, product_name: str) -> str:
    """
    Generates the full Alko image URL for a product.
    """
    numero_str = f"{numero:06d}"  # to 6 digits
    slug = slugify(product_name)
    return ALKO_IMAGE_BASE_URL.format(numero=numero_str, slug=slug)


def main():
    # Load Excel
    df = pd.read_excel(INPUT_FILE, header=3)

    # Ensure columns exist
    if "Numero" not in df.columns or "Nimi" not in df.columns:
        raise ValueError("Excel file must contain 'Numero' and 'Nimi' columns.")

    # Generate URLs
    df["ImageURL"] = df.apply(lambda row: generate_image_url(int(row["Numero"]), str(row["Nimi"])), axis=1)

    # Save to Excel
    df[["Numero", "Nimi", "ImageURL"]].to_excel(OUTPUT_FILE, index=False)
    print(f"Generated image URLs saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
