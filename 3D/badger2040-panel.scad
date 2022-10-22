// -----------------------------------------------------------------------------
// 3D-Model (OpenSCAD) for a Badger2040.
//
// This model is the front panel.
//
// Author: Bernhard Bablok
// License: GPL3
//
// https://github.com/bablokb/circuitpython-clock
//
// ---------------------------------------------------------------------------

include <dimensions.scad>
include <BOSL2/std.scad>

x1_panel = 85.6 + 2*w2;            // outer dimension
x2_panel = 81.5 + w2;              // dimension full z-height
x3_panel = 66.9;                   // dimension inner cutout
x3_panel_off = 9.35 + w2;          //    offset

y1_panel = 48.7 + 2*w2;            // outer dimension
y2_panel = 39.3;                   // dimension full z-height
y3_panel = 29.06;                  // dimension inner cutout

z2_panel = 1.6;                    // panel depth above pcb
z3_panel = 0.4;                    // panel depth above display
z_panel  = z2_panel + z3_panel;

r_panel = 3;                       // panel rounding

d_panel_cyl     = 1.9;             // diameter cylinders for montage holes
h_panel_cyl     = 1.8;             // hight    cylinders for montage holes
d_panel_cyl_off = 2.9 + w2;        // offsets center of holes

g_button     = 0.2;                // gap around buttons
x_button     = 4.2 + 2*g_button;   // width of button
x_button_off = 24;                 // offset in x-dimension from center for horizontal buttons
y_button     = 3.2 + 2*g_button;   // depth of button
y_button_off = 7.27;               // offset in y-dimension from center for vertical buttons

// --- the base plate with cutouts   --------------------------------------------------------------

module plate() {
  difference() {
    cuboid([x1_panel,y1_panel,z_panel],
            rounding=r_panel, anchor=BOTTOM+CENTER,
            edges="Z");
    translate([-(x1_panel-x2_panel)/2,0,-fuzz])
      cuboid([x2_panel,y2_panel,z2_panel+fuzz],
              anchor=BOTTOM+CENTER);
    translate([0,0,-fuzz])
      cuboid([x3_panel,y3_panel,z_panel+2*fuzz],
              anchor=BOTTOM+CENTER);
  }
}

// --- four cylinders for the montage holes   ----------------------------------------------------
  
module montage_cyls() {
  x_off = x1_panel/2-d_panel_cyl_off;
  y_off = y1_panel/2-d_panel_cyl_off;
  translate([-x_off,-y_off,0]) cylinder(d=d_panel_cyl,h=h_panel_cyl,anchor=TOP+CENTER);
  translate([-x_off,+y_off,0]) cylinder(d=d_panel_cyl,h=h_panel_cyl,anchor=TOP+CENTER);
  translate([+x_off,-y_off,0]) cylinder(d=d_panel_cyl,h=h_panel_cyl,anchor=TOP+CENTER);
  translate([+x_off,+y_off,0]) cylinder(d=d_panel_cyl,h=h_panel_cyl,anchor=TOP+CENTER);
}

// --- cutout for buttons   ----------------------------------------------------------------------

module button(orient="H") {
  if (orient == "H") {
    translate([0,0,-fuzz]) cuboid([x_button,y_button,z_panel+2*fuzz],anchor=BOTTOM+CENTER);
  } else {
    translate([0,0,-fuzz]) cuboid([y_button,x_button,z_panel+2*fuzz],anchor=BOTTOM+CENTER);
  }
}

module buttons() {
  y_off_abc = -y1_panel/2 + d_panel_cyl_off;
  translate([-x_button_off,y_off_abc,0]) button();                        // button a
  translate([0,            y_off_abc,0]) button();                        // button b
  translate([+x_button_off,y_off_abc,0]) button();                        // button c

  x_off_du = x1_panel/2 - d_panel_cyl_off;
  translate([x_off_du,-y_button_off,0]) button("V");                      // down
  translate([x_off_du,+y_button_off,0]) button("V");                      // up
}

// --- final frame   -----------------------------------------------------------------------------

module frame() {
  difference() {
    union() {
      plate();
      montage_cyls();
    }
    buttons();
  }
}

frame();
