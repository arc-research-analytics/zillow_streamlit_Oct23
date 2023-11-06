# function to convert hex values to RGB
def hex_to_rgb(hex_color):
    # Convert a hex color (e.g., "#RRGGBB") to an RGB tuple
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


# function to generate an RGB choropleth color ramp based on hex inputs
def generate_color_gradients(start_color, end_color, num_steps):
    # Convert hex colors to RGB tuples
    start_rgb = hex_to_rgb(start_color)
    end_rgb = hex_to_rgb(end_color)

    # Generate step-wise gradients
    gradients = []
    for step in range(num_steps):
        # Interpolate between start and end colors
        r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0])
                * step / (num_steps - 1))
        g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1])
                * step / (num_steps - 1))
        b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2])
                * step / (num_steps - 1))
        gradient_color = (r, g, b)
        gradients.append(gradient_color)

    return gradients
