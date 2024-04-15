from PIL import Image
import array
import cProfile


x1,x2,y1,y2 = -1.8, 1.8, -1.8, 1.8
c_real, c_imag = -0.62772, -.42193

def show_greyscale(output, width, height, max_iterations):
    max_iterations = float(max(output))
    print("Max iterations:", max_iterations)
    scale_factor = float(max_iterations)
    print("Scale factor:", scale_factor)
    scaled = [int(o/scale_factor*255) for o in output]
    output = array.array('B', scaled)
    #output = output.tostring()
    img = Image.frombytes("L", (width, height), output)
    img.show()

def show_false_greyscale(output, width, height, max_iterations):
    assert width * height == len(output)
    max_value = float(max(output))
    output_raw_limited = [int(float(o) / max_value * 255) for o in output]
    output_rgb = ((o+(256*o)+(256**2)*o) for o in output_raw_limited)
    output_rgb = array.array('I', output_rgb)
    img = Image.new("RGB", (width, height))
    img.frombytes(output_rgb.tobytes(), 'raw', "RGBX", 0, -1)
    img.show()

def calculate_z_serial_purepython(maxiter, zs, cs):
    output = [0] * len(zs)
    for i in range(len(zs)):
        n = 0
        z = zs[i]
        c = cs[i]
        while abs(z) < 2 and n < maxiter:
            z = z * z + c
            n += 1
        output[i] = n
    return output

def calc_pure_python(desired_width, max_iterations):
    x_step = (float(x2-x1) / float(desired_width))
    y_step = (float(y1-y2) / float(desired_width))
    x = []
    y = []
    ycoord = y2
    while ycoord > y1:
        y.append(ycoord)
        ycoord += y_step
    xcoord = x1
    while xcoord < x2:
        x.append(xcoord)
        xcoord += x_step
    zs = []
    cs = []
    for ycoord in y:
        for xcoord in x:
            zs.append(complex(xcoord, ycoord))
            cs.append(complex(c_real, c_imag))
    print("Total of %d elements" % len(zs))
    print("Length of x:", len(x))
    output = calculate_z_serial_purepython(max_iterations, zs, cs)

    assert sum(output) == 33219980


def start():
    cProfile.run("calc_pure_python(desired_width=1000, max_iterations=300)", sort="time")