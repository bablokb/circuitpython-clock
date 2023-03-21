// -----------------------------------------------------------------------------
// 3D-Model (OpenSCAD) for a Badger2040.
//
// This model is the bottom support.
//
// Author: Bernhard Bablok
// License: GPL3
//
// https://github.com/bablokb/circuitpython-clock
//
// -----------------------------------------------------------------------------

include <dimensions.scad>
include <BOSL2/std.scad>

t_support = y_support_bot-2*w4 - (y_support_top-2*w4);
alpha = atan(t_support/h_support);                       // angle of corpus

// --- the corpus   ------------------------------------------------------------

module corpus() {
  rect_tube(size1=[x1_panel,y_support_bot],size2=[x1_panel,y_support_top],
                   h=h_support,wall=w4,shift=[0,-y_support_shift],
                   rounding=r_panel,irounding=r_panel,anchor=BOTTOM+CENTER);
}

// --- cutouts   -------------------------------------------------------------

module cutouts() {
  y_off_support = -(y_support_bot/2-w4/2)-fuzz;
  // cable hole
  translate([+1.5*x_cable,y_off_support,(z_body-z_cable)/2])
       cuboid([x_cable,w4+2*fuzz,z_cable],anchor=BOTTOM+CENTER);

  // lipo-pro
  translate([0,
             y_support_bot/2-w4-(h_support-y_holder)*t_support/h_support,
             h_support-y_holder])
    xrot(alpha) cuboid([x_holder+2*gap,w4,y_holder+4*gap],anchor=BOTTOM+CENTER);

  // base-connector
  translate([-x1_panel/2+x1_panel/8,y_off_support,z_bcon_off])
       cuboid([x_bcon+gap/2,y_bcon+2*fuzz,z_bcon],anchor=BOTTOM+CENTER);
  translate([+x1_panel/2-x1_panel/8,y_off_support,z_bcon_off])
       cuboid([x_bcon+gap/2,y_bcon+2*fuzz,z_bcon],anchor=BOTTOM+CENTER);
}

// --- final model   ---------------------------------------------------------

module support() {
  difference() {
    corpus();
    cutouts();
  }
}

support();
