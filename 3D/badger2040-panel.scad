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

x1_panel = 86.2 + 2*w2;            // outer dimension
x2_panel = 79.7 + w2;              // dimension full z-height
x3_panel = 66.9;                   // dimension inner cutout
x3_panel_off = 9.35 + w2;          //    offset

y1_panel = 48.7 + 2*w2;            // outer dimension
y2_panel = 37.2;                   // dimension full z-height
y2_panel_off = 5.8 + w2;           //    offset
y3_panel = 29.06;                  // dimension inner cutout
y3_panel_off = 10.15 + w2;         //    offset

z2_panel = 1.6;                    // panel depth above pcb
z3_panel = 0.4;                    // panel depth above display
z_panel  = z2_panel + z3_panel;

r_panel = 3;                       // panel rounding

d_panel_cyl     = 1.9;             // diameter cylinders for montage holes
h_panel_cyl     = 1.8;             // hight    cylinders for montage holes
d_panel_cyl_off = 2.9 + w2;        // offsets center of holes

g_button     = 0.1;                // gap around buttons
x_button     = 4.2 + 2*g_button;   // width of button
x_button_off = 16.7-g_button+w2;   // offset in  x-dimension for horizontal buttons
x_button_o   = 2.1+g_button+w2;    // offset from rim vertical buttons
y_button     = 3.2 + 2*g_button;   // depth of button
y_button_off = 14.99-g_button+w2;  // offset in y-dimensions for vertical buttons
y_button_o   = 1.3+g_button+w2;    // offset from rim horizontal buttons

// --- the base plate with cutouts   --------------------------------------------------------------

module plate() {
  difference() {
    cuboid([x1_panel,y1_panel,z_panel],
            rounding=r_panel, anchor=BOTTOM+FRONT+LEFT,
            edges="Z");
    translate([0,y2_panel_off,-fuzz])
      cuboid([x2_panel,y2_panel,z2_panel+fuzz],
              anchor=BOTTOM+FRONT+LEFT);
    translate([x3_panel_off,y3_panel_off,-fuzz])
      cuboid([x3_panel,y3_panel,z_panel+2*fuzz],
              anchor=BOTTOM+FRONT+LEFT);
  }
}

// --- four cylinders for the montage holes   ----------------------------------------------------
  
module montage_cyls() {
  translate([d_panel_cyl_off,d_panel_cyl_off,0])
     cylinder(d=d_panel_cyl,h=h_panel_cyl,anchor=TOP+FRONT+LEFT);
  translate([x1_panel-d_panel_cyl-d_panel_cyl_off,d_panel_cyl_off,-fuzz])
     cylinder(d=d_panel_cyl,h=h_panel_cyl,anchor=TOP+FRONT+LEFT);
  translate([d_panel_cyl_off,y1_panel-d_panel_cyl-d_panel_cyl_off,-fuzz])
     cylinder(d=d_panel_cyl,h=h_panel_cyl,anchor=TOP+FRONT+LEFT);
  translate([x1_panel-d_panel_cyl-d_panel_cyl_off,y1_panel-d_panel_cyl-d_panel_cyl_off,-fuzz])
     cylinder(d=d_panel_cyl,h=h_panel_cyl,anchor=TOP+FRONT+LEFT);
}

// --- cutout for buttons   ----------------------------------------------------------------------

module button(orient="H") {
  if (orient == "H") {
    translate([0,0,-fuzz]) cuboid([x_button,y_button,z_panel+2*fuzz],anchor=BOTTOM+FRONT);
  } else {
    translate([0,0,-fuzz]) cuboid([y_button,x_button,z_panel+2*fuzz],anchor=BOTTOM+CENTER);
  }
}

module buttons() {
  translate([x_button_off+x_button/2,y_button_o,0]) button();             // button a
  translate([x1_panel/2,y_button_o,0]) button();                          // button b
  translate([x1_panel-x_button/2-x_button_off,y_button_o,0]) button();    // button c
  translate([x1_panel-y_button/2-x_button_o,
                     y_button_off+x_button/2,0]) button("V");             // down
  translate([x1_panel-y_button/2-x_button_o,
                     y1_panel-x_button/2-y_button_off,0]) button("V");    // up  
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
