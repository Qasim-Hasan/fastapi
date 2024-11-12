from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os

router = APIRouter()

# Global variable to hold the received data type
received_data_type: str = "synop"  # Default data type

# Request model for the data type
class DataTypeRequest(BaseModel):
    datatype: str

@router.post("/data-type", response_model=dict, status_code=201)
async def receive_data_type(data: DataTypeRequest):
    global received_data_type  # Declare the global variable
    received_data_type = data.datatype  # Update the data type
    print(f"Received data type: {received_data_type}")
    return {"message": "Data type received successfully", "datatype": received_data_type}

@router.get("/image-data")
def get_image_data(
    image_type: str = Query(..., description="Type of image requested (e.g., 'isobar', 'isotherm', 'isoneph')")
):
    base_url = os.getenv("BASE_URL", "http://3.110.124.113:8000")  # Use EC2 public IP
    
    # Check if the current data type is 'synop'
    if received_data_type == "synop":
        # Hardcoded URLs for the images using EC2's public IP
        if image_type == "isobar":
            layer_image_url = f"{base_url}/assets/isobars.png"
            heatmap_image_url = f"{base_url}/assets/isobars_heatmap.png"
        elif image_type == "isotherm":
            layer_image_url = f"{base_url}/assets/isotherms.png"
            heatmap_image_url = f"{base_url}/assets/isotherms_heatmap.png"
        elif image_type == "isoneph":
            layer_image_url = f"{base_url}/assets/isonephs.png"
            heatmap_image_url = f"{base_url}/assets/isonephs_heatmap.png"
        else:
            return JSONResponse(content={"error": "Invalid image type"}, status_code=400)

        # Define coordinates (bounds)
        coordinates = {
            "bounds": [
                [60.87, 23.63],
                [77.05, 37.23]
            ]
        }

        # Construct the response data
        data = {
            "layer_image_url": layer_image_url,
            "heatmap_image_url": heatmap_image_url,
            "coordinates": coordinates
        }

        return JSONResponse(content=data)

    # Handle the cases for 'metar' and 'wis2'
    elif received_data_type in ["metar", "wis2"]:
        return JSONResponse(content={"error": "No image data available for the requested data type."}, status_code=204)

    # If the data type is not recognized
    return JSONResponse(content={"error": "Invalid data type."}, status_code=400)
