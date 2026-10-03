import nuke

# Adds the Astigmatism gizmo to the Nodes toolbar. Nuke picks this file up
# automatically when the folder that contains it is on the plugin path.

lens = nuke.menu("Nodes").addMenu("Lens")
lens.addCommand("Astigmatism", "nuke.createNode('Astigmatism')")
