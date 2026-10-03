# Reads the Blink kernel source and writes Astigmatism.gizmo with the kernel
# embedded and a set of user knobs driving it.

SRC = "astigmatism/Astigmatism.blink"
DST = "Astigmatism.gizmo"

kernel = open(SRC).read()
escaped = (kernel
    .replace("\\", "\\\\")
    .replace('"', '\\"')
    .replace("{", "\\{")
    .replace("}", "\\}")
    .replace("\n", "\\n"))

# Group-level knobs, in panel order. Each Blink parameter is then driven by an
# expression pointing at the matching group knob.
panel = """ addUserKnob {20 Astigmatism}
 addUserKnob {26 about l "The blur is the lens aperture stretched into an ellipse. It is smallest and round at the circle of least confusion, and collapses to a short line at either end of Focus." +STARTLINE}
 addUserKnob {12 center l "Optical Center" t "The point the effect radiates from. Only used when Track Format Center is off."}
 center {960 540}
 addUserKnob {6 centerOnFormat l "Track Format Center" -STARTLINE t "Keep the optical centre in the middle of the format. Turn off to place it with Optical Center."}
 centerOnFormat true
 addUserKnob {7 amount l "Amount (px)" t "Radius, in pixels, of the circle of least confusion at the corner of the frame. The line foci are twice this long." R 0 300}
 amount 15
 addUserKnob {7 focus l Focus t "Where the sensor sits between the two astigmatic foci. -1 is the sagittal focus, highlights streak outward like spokes. 0 is the circle of least confusion, the blur is round and at its smallest. +1 is the tangential focus, highlights streak around the centre." R -1 1}
 focus -0.5
 addUserKnob {26 field l FIELD +STARTLINE}
 addUserKnob {7 falloffPower l "Falloff Power" t "How fast the blur grows away from the centre. 2 matches the physics of primary astigmatism, where it grows with the square of the field angle." R 0 6}
 falloffPower 2
 addUserKnob {7 innerRadius l "Inner Radius" t "Normalised distance from the centre at which the effect starts. 0 means it begins at the optical centre." R 0 1}
 innerRadius 0
 addUserKnob {7 aspect l "Field Aspect" t "Stretches the falloff shape vertically. Raise it for an anamorphic frame where the blur should grow faster toward the top and bottom." R 0.25 4}
 aspect 1
 addUserKnob {26 lens l LENS +STARTLINE}
 addUserKnob {3 blades l "Aperture Blades" t "Number of iris blades. 0 keeps the aperture round. 5 to 8 give straight-sided bokeh." R 0 12}
 blades 0
 addUserKnob {7 bladeRotation l "Blade Rotation" -STARTLINE t "Rotates the iris, in degrees." R 0 360}
 bladeRotation 0
 addUserKnob {7 vignetting l "Optical Vignetting" t "Pinches out-of-focus highlights into a cat's eye toward the edges of the frame, the way a real lens barrel cuts the aperture." R 0 1.5}
 vignetting 0.5
 addUserKnob {7 bokehRim l "Bokeh Outline" t "Brightens the rim of the aperture so highlights pick up an outlined edge." R 0 3}
 bokehRim 0.8
 addUserKnob {7 edgeSoftness l "Edge Softness" t "How softly the aperture edge rolls off. Low values give a crisp iris, high values a gentle one." R 0 1}
 edgeSoftness 0.3
 addUserKnob {7 chroma l "Colour Fringing" t "Longitudinal colour. Positive values let the red blur grow larger than the blue, giving the coloured edge real lenses show." R -1 1}
 chroma 0
 addUserKnob {26 quality l QUALITY +STARTLINE}
 addUserKnob {3 samples l Samples t "Samples taken per pixel. Raise it if bright highlights show grain. Cost scales directly with this." R 1 256}
 samples 64
 addUserKnob {7 minWidth l "Minimum Width" t "The thinnest the blur ellipse is allowed to get, in pixels, so a line focus stays a soft line rather than a hard one." R 0 5}
 minWidth 0.75
 addUserKnob {7 jitter l Dither t "Breaks up the sample pattern into fine grain. Turn it down for a smoother, more clinical result." R 0 2}
 jitter 1
 addUserKnob {7 mix l Mix t "Blends the effect back to the original image." R 0 1}
 mix 1
 addUserKnob {6 processAlpha l "Process Alpha" -STARTLINE t "Blur the alpha with the colour. Turn off to leave the alpha untouched."}
 processAlpha true
 addUserKnob {4 debugView l "Debug View" M {Result Falloff "Ellipse Axes"} t "Falloff shows how the blur strength grows across the frame. Ellipse Axes shows the radial blur in red and the tangential blur in green."}
 debugView Result"""

# Expressions on the BlinkScript node, one per kernel parameter.
links = {
    "center": "{{parent.center.x} {parent.center.y}}",
    "centerOnFormat": "{{parent.centerOnFormat}}",
    "formatSize": "{{format.w} {format.h}}",
    "pixelAspect": "{{format.pixel_aspect}}",
    "amount": "{{parent.amount}}",
    "focus": "{{parent.focus}}",
    "falloffPower": "{{parent.falloffPower}}",
    "innerRadius": "{{parent.innerRadius}}",
    "aspect": "{{parent.aspect}}",
    "samples": "{{parent.samples}}",
    "edgeSoftness": "{{parent.edgeSoftness}}",
    "blades": "{{parent.blades}}",
    "bladeRotation": "{{parent.bladeRotation}}",
    "vignetting": "{{parent.vignetting}}",
    "bokehRim": "{{parent.bokehRim}}",
    "minWidth": "{{parent.minWidth}}",
    "chroma": "{{parent.chroma}}",
    "jitter": "{{parent.jitter}}",
    "mix": "{{parent.mix}}",
    "processAlpha": "{{parent.processAlpha}}",
    "debugView": "{{parent.debugView}}",
}

link_lines = "\n".join("  %s %s" % (name, expr) for name, expr in links.items())

gizmo = """version 16.0 v1
Gizmo {{
 inputs 1
 name Astigmatism
{panel}
}}
 Input {{
  inputs 0
  name Input
  xpos 0
  ypos -100
 }}
 BlinkScript {{
  kernelSource "{kernel}"
  useGPUIfAvailable true
  name AstigmatismKernel
  xpos 0
  ypos 0
{links}
 }}
 Output {{
  name Output1
  xpos 0
  ypos 100
 }}
end_group
""".format(panel=panel, kernel=escaped, links=link_lines)

open(DST, "w").write(gizmo)
print("wrote", DST, "chars", len(gizmo))
