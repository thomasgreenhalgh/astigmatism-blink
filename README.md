# Astigmatism

A Nuke gizmo that reproduces lens astigmatism. It runs on Nuke 14 and later, on any licence, and does its work in a BlinkScript kernel that uses the GPU.

## What it does

A lens with astigmatism focuses the rays in two perpendicular directions at two different depths, so a point of light off the centre of frame is never rendered as a point. It is rendered as the shape of the aperture, stretched into an ellipse.

The **Focus** slider moves the sensor between those two depths:

- **-1, sagittal focus.** Highlights stretch into short lines pointing outward from the centre, like spokes.
- **0, circle of least confusion.** The blur is round, and this is where it is smallest.
- **+1, tangential focus.** Highlights stretch into short lines that run around the centre.

The blur grows with the square of the distance from the optical centre, so the middle of the frame stays sharp and the corners fall apart, which is how astigmatism behaves in a real lens. The lines at either focus are twice as long as the circle of least confusion is wide.

Because the kernel normalises its samples, flat areas of colour pass through unchanged. Only detail and bright highlights take on the ellipse, the way a real defocused lens looks.

## Install

1. In Nuke, open **Edit > Preferences > Behaviors > Plugin** and add this folder to the plugin path.
2. Restart Nuke.

The node appears in the Nodes toolbar under **Lens > Astigmatism**.

If you would rather not install it, copy `Astigmatism.gizmo` into `~/.nuke/` instead. It loads from there without the menu entry.

## Controls

**Focus**

- **Optical Center** and **Track Format Center.** The point the effect radiates from. Tracking keeps it in the middle of the frame; untick it to drag the centre somewhere else.
- **Amount.** The radius of the circle of least confusion at the corner of the frame, in pixels. Start around 15 and push it until the corners feel right. The line foci end up twice this long.
- **Focus.** The slider described above.

**Field**

- **Falloff Power.** How quickly the blur grows toward the edges. Leave it at 2 for the physical result.
- **Inner Radius.** Holds the centre perfectly sharp out to this fraction of the frame.
- **Field Aspect.** Stretches the falloff vertically, for anamorphic material where the top and bottom should soften before the sides.

**Lens**

- **Aperture Blades** and **Blade Rotation.** 0 keeps a round aperture. 5 to 8 give straight-sided bokeh, rotated by the blade control.
- **Optical Vignetting.** Pinches highlights into a cat's eye toward the edges, where the lens barrel cuts the aperture.
- **Bokeh Outline.** Puts a bright rim on the aperture so highlights read as outlined.
- **Edge Softness.** A low value is a crisp iris, a high value a gentle one.
- **Colour Fringing.** Lets the red blur grow larger than the blue, which gives the coloured edge a real lens shows. 0 keeps it neutral.

**Quality**

- **Samples.** Samples per pixel. The default of 64 is smooth on most images; raise it if bright specular highlights look grainy. The render cost scales with this number.
- **Minimum Width.** Stops a line focus from collapsing to a hard one-pixel line.
- **Dither.** Turns the sample pattern into fine grain. Lower it for a cleaner, more clinical result.
- **Mix.** Blends the effect back to the original.
- **Process Alpha.** Blurs the alpha along with the colour.
- **Debug View.** *Falloff* shows where the blur lands across the frame. *Ellipse Axes* shows the radial blur in red and the tangential blur in green, which is useful for seeing exactly what the Focus slider is doing.

## Tips

- The effect is meant to be subtle. If the whole frame looks smeared, the Amount is too high or the Focus is pinned at -1 or +1. Pull Focus back toward 0 for ellipses rather than lines.
- For the classic look of point lights breaking into ellipses and streaks at the edges, grade the highlights up before the node so the aperture shape has something bright to draw.
- It is a gather blur, so it stays fast on the GPU. On the CPU, lower Samples while you set it up.

## Files

- `Astigmatism.gizmo` is the node, with the kernel embedded in it.
- `astigmatism/Astigmatism.blink` is the kernel source. After editing it, regenerate the gizmo with `python3 .scratch/build_gizmo.py`.
- `menu.py` adds the toolbar entry.
