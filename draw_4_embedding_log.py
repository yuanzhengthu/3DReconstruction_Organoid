import os
import re
import matplotlib.pyplot as plt
from matplotlib import rcParams

def parse_log_file(log_path):
    ssim_values = []
    psnr_values = []
    reconstruction_times = []

    with open(log_path, 'r') as log_file:
        lines = log_file.readlines()

        for line in lines:
            # Parse SSIM
            ssim_match = re.search(r'SSIM for image 0: (\d+\.\d+)', line)
            if ssim_match:
                ssim_values.append(float(ssim_match.group(1)))

            # Parse PSNR
            psnr_match = re.search(r'PSNR for image 0: (\d+\.\d+)', line)
            if psnr_match:
                psnr_values.append(float(psnr_match.group(1)))

            # Parse Reconstruction Time
            reconstruction_time_match = re.search(r': (\d+\.\d+) seconds', line)
            if reconstruction_time_match:
                reconstruction_times.append(float(reconstruction_time_match.group(1)))

    return ssim_values, psnr_values, reconstruction_times

def plot_metrics(subdirectories, ssim_data, psnr_data, reconstruction_time_data):
    # Set font properties
    rcParams['font.family'] = 'serif'
    rcParams['font.serif'] = ['Times New Roman']
    rcParams['font.size'] = 18

    # markers = ['*', 's', '^', 'D', 'o']  # You can add more markers as needed
    markers = ['s', '^', '.', 'x', 'v']
    colors = ['Orange', 'green', 'Purple', 'Brown', 'Black']
    # Plot SSIM
    plt.figure(figsize=(15, 5))
    plt.subplot(1, 3, 1)
    for i, (subdir, ssim_values) in enumerate(zip(subdirectories, ssim_data)):
        plt.plot(ssim_values[::2], marker=markers[i % len(markers)], linestyle='', label=subdir, alpha=0.5, color=colors[i % len(colors)])
    plt.title('SSIM')
    plt.legend()

    # Plot PSNR
    plt.subplot(1, 3, 2)
    for i, (subdir, psnr_values) in enumerate(zip(subdirectories, psnr_data)):
        plt.plot(psnr_values[::2], marker=markers[i % len(markers)], linestyle='', label=subdir, alpha=0.5, color=colors[i % len(colors)])
    plt.title('PSNR')
    # plt.legend()

    # Plot Reconstruction Time
    plt.subplot(1, 3, 3)
    for i, (subdir, reconstruction_times) in enumerate(zip(subdirectories, reconstruction_time_data)):
        plt.plot(reconstruction_times[::2], marker=markers[i % len(markers)], linestyle='', label=subdir, alpha=0.5, color=colors[i % len(colors)])
    plt.title('Reconstruction Time')
    # plt.legend()

    # Save the figure with high resolution
    plt.tight_layout()
    plt.savefig('metrics_plot.png', dpi=1200)
    plt.show()

# Directory containing subdirectories with test.log files
base_dir = 'draw_log_compare_quantization'

subdirectories = []
ssim_data = []
psnr_data = []
reconstruction_time_data = []

# Iterate over subdirectories
for subdir in os.listdir(base_dir):
    subdir_path = os.path.join(base_dir, subdir)
    if os.path.isdir(subdir_path):
        # Find the test.log file in each subdirectory
        log_file_path = os.path.join(subdir_path, 'test.log')

        # Parse and store metrics
        ssim_values, psnr_values, reconstruction_times = parse_log_file(log_file_path)
        subdirectories.append(subdir)
        ssim_data.append(ssim_values)
        psnr_data.append(psnr_values)
        reconstruction_time_data.append(reconstruction_times)

# Plot even indices for different subdirectories with different markers and save the figure
plot_metrics(subdirectories, ssim_data, psnr_data, reconstruction_time_data)
