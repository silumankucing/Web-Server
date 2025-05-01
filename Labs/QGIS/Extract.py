from qgis.core import (
    QgsProject,
    QgsVectorLayer,
    QgsFeature
)
import csv

# Function to extract data from a vector layer and save to CSV
def extract_layer_to_csv(layer_name, output_csv_path):
    # Get the active QGIS project
    project = QgsProject.instance()

    # Find the layer by name
    layer = project.mapLayersByName(layer_name)
    if not layer:
        print(f"Layer '{layer_name}' not found!")
        return
    layer = layer[0]

    # Check if the layer is a vector layer
    if not isinstance(layer, QgsVectorLayer):
        print(f"Layer '{layer_name}' is not a vector layer!")
        return

    # Open a CSV file for writing
    with open(output_csv_path, mode='w', newline='', enco ding='utf-8') as csv_file:
        writer = csv.writer(csv_file)

        # Write the header (field names)
        fields = [field.name() for field in layer.fields()]
        writer.writerow(fields)

        # Write the feature data
        for feature in layer.getFeatures():
            writer.writerow([feature[field] for field in fields])

    print(f"Data from layer '{layer_name}' has been exported to '{output_csv_path}'.")

# Example usage
layer_name = "YourLayerName"  # Replace with the name of your layer
output_csv_path = "d:/Artificial Intelligence/Labs/QGIS/output.csv"  # Replace with your desired output path
extract_layer_to_csv(layer_name, output_csv_path)