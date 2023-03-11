// -----------------------------------------------------------------------------
// 3D-Model (OpenSCAD) for a Badger2040.
//
// This model is for the connector between top and bottom part. You need this
// part twice.
//
// Author: Bernhard Bablok
// License: GPL3
//
// https://github.com/bablokb/circuitpython-clock
//
// -----------------------------------------------------------------------------

include <dimensions.scad>
include <BOSL2/std.scad>

// --- connector (need to be glued into support)   ---------------------------

module connector() {
  // cutouts are: x_bcon+gap/2 and z_bcon
  xdim = x_bcon - gap/2;
  ydim = z_bcon - gap;
  fwd(ydim/2) xrot(-90) cuboid([xdim,7,ydim],anchor=BACK+BOTTOM+CENTER);
   cuboid([10,ydim,0.6],anchor=TOP+CENTER);
}

// --- final model   ---------------------------------------------------------

connector();
