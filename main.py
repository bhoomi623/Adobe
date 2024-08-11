import numpy as np
import matplotlib.pyplot as plt
import svgwrite
from PIL import Image
import io
import csv

# Function to generate a sample CSV file with polyline data
def generate_sample_csv(csv_path):
    data = [
        [0, 1, 1],
        [0, 2, 2],
        [0, 3, 3],
        [1, 1, 1],
        [1, 4, 4],
        [1, 5, 5],
        [2, 2, 2],
        [2, 6, 6],
        [2, 7, 7]
    ]
    with open(csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['PathID', 'PointID', 'X', 'Y'])
        for row in data:
            writer.writerow(row)

# Function to read CSV file
def read_csv(csv_path):
    np_path_XYs = np.genfromtxt(csv_path, delimiter=',', skip_header=1)
    path_XYs = []
    for i in np.unique(np_path_XYs[:, 0]):
        npXYs = np_path_XYs[np_path_XYs[:, 0] == i][:, 1:]
        XYs = []
        for j in np.unique(npXYs[:, 0]):
            XY = npXYs[npXYs[:, 0] == j][:, 1:]
            XYs.append(XY)
        path_XYs.append(XYs)
    return path_XYs

# Function to plot paths
def plot(paths_XYs, svg_path='output.svg'):
    fig, ax = plt.subplots(tight_layout=True, figsize=(8, 8))
    colours = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    for i, XYs in enumerate(paths_XYs):
        c = colours[i % len(colours)]
        for XY in XYs:
            if XY.shape[0] > 1:  # Skip plotting single points
                ax.plot(XY[:, 0], XY[:, 1], c=c, linewidth=2)
    ax.set_aspect('equal')
    plt.savefig(svg_path, format='svg')
    plt.close()

# Function to save SVG as PNG
def svg_to_png(svg_path, png_path):
    dwg = svgwrite.Drawing(png_path, (800, 800))
    dwg.add(dwg.image(svg_path, insert=(0, 0), size=(800, 800)))
    dwg.save()

# Main function
def main():
    csv_file_path = 'shapes_data.csv'
    svg_file_path = 'output.svg'
    png_file_path = 'output.png'

    generate_sample_csv(csv_file_path)
    path_XYs = read_csv(csv_file_path)
    plot(path_XYs, svg_path=svg_file_path)
    svg_to_png(svg_file_path, png_file_path)
    print("Project completed successfully.")

if __name__ == "__main__":
    main()