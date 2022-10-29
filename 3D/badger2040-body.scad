// -----------------------------------------------------------------------------
// 3D-Model (OpenSCAD) for a Badger2040.
//
// This model is the main body.
//
// Author: Bernhard Bablok
// License: GPL3
//
// https://github.com/bablokb/circuitpython-clock
//
// -----------------------------------------------------------------------------

include <dimensions.scad>
include <BOSL2/std.scad>

// --- the corpus   ------------------------------------------------------------

module corpus() {
    difference() {
    cuboid([x1_panel,y1_panel,z_body],
            rounding=r_panel, anchor=BOTTOM+CENTER,
            edges="Z");
    translate([0,0,-fuzz])
      cuboid([x1_panel-2*w4,y1_panel-2*w4,z_body+2*fuzz],
              rounding=r_panel, anchor=BOTTOM+CENTER,
              edges="Z");
  }
}

// --- cutouts   -------------------------------------------------------------

module cutouts() {
  // usb-c connector
  translate([-x1_panel/2+w4/2-fuzz,
             -y1_panel/2+y_usb_off,z_body-z_usb+fuzz])
       cuboid([w4+2*fuzz,y_usb,z_usb+fuzz],anchor=BOTTOM+CENTER);

  // back buttons
  translate([-x1_panel/2+x_bb_off,y1_panel/2-w4/2-fuzz,z_body-z_bb+fuzz])
       cuboid([x_bb,w4+2*fuzz,z_bb+fuzz],anchor=BOTTOM+CENTER);

  // base-connector
  translate([-x1_panel/2+x1_panel/4,
             -y1_panel/2+w4/2-fuzz,z_bcon_off])
       cuboid([w4+gap/2,w4+2*fuzz,z_bcon],anchor=BOTTOM+CENTER);
  translate([+x1_panel/2-x1_panel/4,
             -y1_panel/2+w4/2-fuzz,z_bcon_off])
       cuboid([w4+gap/2,w4+2*fuzz,z_bcon],anchor=BOTTOM+CENTER);

  // cable hole
  translate([0,-y1_panel/2+w4/2-fuzz,(z_body-z_cable)/2])
       cuboid([x_cable,w4+2*fuzz,z_cable],anchor=BOTTOM+CENTER);
  
}

// --- final model   ---------------------------------------------------------

module body() {
  difference() {
    corpus();
    cutouts();
  }
}

body();
