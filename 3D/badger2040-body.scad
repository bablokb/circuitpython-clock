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

// --- back-button cover   ---------------------------------------------------

module bb_cover() {
  x_dim = x_bb+2*w2;
  y_dim = y_bb+2*w2;
  zrot(180) yrot(180) union() {
    rect_tube(size=[x_dim,y_dim],wall=w2,h=h_bb);
    zrot(90) translate([0,0,h_bb]) difference() {
      prismoid(size1=[y_dim,x_dim],
               size2=[0,x_dim], shift=[-y_dim/2,0], h=x_dim);
      prismoid(size1=[y_dim-2*w2,x_dim-2*w2],
               size2=[0,x_dim-2*w2], shift=[-(y_dim-2*w2)/2-h_bb_off/2,0], h=x_dim-4*w2);
    }
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
  translate([-x1_panel/2+x1_panel/8,
             -y1_panel/2+w4/2-fuzz,z_bcon_off])
       cuboid([w4+gap/2,w4+2*fuzz,z_bcon],anchor=BOTTOM+CENTER);
  translate([+x1_panel/2-x1_panel/8,
             -y1_panel/2+w4/2-fuzz,z_bcon_off])
       cuboid([w4+gap/2,w4+2*fuzz,z_bcon],anchor=BOTTOM+CENTER);

  // cable hole
  translate([+1.5*x_cable,-y1_panel/2+w4/2-fuzz,(z_body-z_cable)/2])
       cuboid([x_cable,w4+2*fuzz,z_cable],anchor=BOTTOM+CENTER);
  
}

// --- final model   ---------------------------------------------------------

module body() {
  difference() {
    union() {
      corpus();
      translate([-x1_panel/2+x_bb_off,y1_panel/2-y_bb/2-w4,z_body-h_bb_off]) bb_cover();
    }
    cutouts();
  }
}

body();
