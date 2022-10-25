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
// -----------------------------------------------------------------------------

include <dimensions.scad>
include <BOSL2/std.scad>

rim = w4+ gap + w2 + gap;

x1_panel = 85.6 + 2*rim;           // outer dimension
x2_panel = 81.5 + rim;             // dimension full z-height
x3_panel = 66.9;                   // dimension inner cutout
x3_panel_off = 9.35 + rim;         //    offset

y1_panel = 48.7 + 2*rim;           // outer dimension
y2_panel = 39.3;                   // dimension full z-height
y3_panel = 29.06;                  // dimension inner cutout

z2_panel = 1.6;                    // panel depth above pcb
z3_panel = 0.4;                    // panel depth above display
z_panel  = z2_panel + z3_panel;

r_panel = 3;                       // panel rounding

d_panel_cyl      = 1.9;            // diameter cylinders for montage holes
h_panel_cyl      = 1.8;            // hight    cylinders for montage holes
xy_panel_cyl_off = 2.9 + rim;      // offsets center of holes

g_button     = 0.2;                // gap around buttons
x_button     = 4.2 + 2*g_button;   // width of button
x_button_off = 24;                 // offsets button a+c (from center)
y_button     = 3.2 + 2*g_button;   // depth of button
y_button_off = 7.27;               // offsets buttons up+down (from center)

x_led_off = 12.7 + rim;            // offset of activity-led
y_led_off = xy_panel_cyl_off;

x_wall = x1_panel - 2*w4 - 2*gap;  // outer wall dimensions
y_wall = y1_panel - 2*w4 - 2*gap;
z_wall = 15;

y_usb     =  9.00;                 // y-dim usb-c (mechanical drawing: 8.94)
y_usb_off = 10.15 + rim;           // offset from bottom

x_bb     = 17;                     // x-dim back buttons (min: 12.2)
x_bb_off = 14.5 + rim;             // offset from left

// --- the base plate with cutouts   -------------------------------------------

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

// --- four cylinders for the montage holes   ----------------------------------
  
module montage_cyls() {
  x_off = x1_panel/2-xy_panel_cyl_off;
  y_off = y1_panel/2-xy_panel_cyl_off;
  translate([-x_off,-y_off,0])
                        cylinder(d=d_panel_cyl,h=h_panel_cyl,anchor=TOP+CENTER);
  translate([-x_off,+y_off,0])
                        cylinder(d=d_panel_cyl,h=h_panel_cyl,anchor=TOP+CENTER);
  translate([+x_off,-y_off,0])
                        cylinder(d=d_panel_cyl,h=h_panel_cyl,anchor=TOP+CENTER);
  translate([+x_off,+y_off,0])
                        cylinder(d=d_panel_cyl,h=h_panel_cyl,anchor=TOP+CENTER);
}

// --- walls   -----------------------------------------------------------------

module walls() {
  difference() {
    cuboid([x_wall,y_wall,z_wall],
            rounding=r_panel, anchor=TOP+CENTER,
            edges="Z");
    translate([0,0,fuzz])
            cuboid([x_wall-2*w2,y_wall-2*w2,z_wall+2*fuzz],
                   rounding=r_panel, anchor=TOP+CENTER,
                   edges="Z");
    translate([-x_wall/2,0,fuzz])
             cuboid([rim+fuzz,y2_panel,z_wall+2*fuzz],anchor=TOP+CENTER);
    translate([-x_wall/2+x_bb_off,y_wall/2,fuzz])
             cuboid([x_bb,rim+fuzz,z_wall+2*fuzz],anchor=TOP+CENTER);
  }
}

// --- cutout for activity led   -----------------------------------------------

module led() {
  x_off = -x1_panel/2+x_led_off;
  y_off = -y1_panel/2+y_led_off;
  translate([x_off,y_off,-fuzz])
    cylinder(d=d_panel_cyl,h=z_panel+2*fuzz,anchor=BOTTOM+CENTER);
}

// --- cutout for buttons   ----------------------------------------------------

module button(orient="H") {
  if (orient == "H") {
    translate([0,0,-fuzz])
                cuboid([x_button,y_button,z_panel+2*fuzz],anchor=BOTTOM+CENTER);
  } else {
    translate([0,0,-fuzz])
                cuboid([y_button,x_button,z_panel+2*fuzz],anchor=BOTTOM+CENTER);
  }
}

module buttons() {
  y_off_abc = -y1_panel/2 + xy_panel_cyl_off;
  translate([-x_button_off,y_off_abc,0]) button();     // button a
  translate([0,            y_off_abc,0]) button();     // button b
  translate([+x_button_off,y_off_abc,0]) button();     // button c

  x_off_du = x1_panel/2 - xy_panel_cyl_off;
  translate([x_off_du,-y_button_off,0]) button("V");   // down
  translate([x_off_du,+y_button_off,0]) button("V");   // up
}

// --- final frame   -----------------------------------------------------------

module frame() {
  difference() {
    union() {
      plate();
      montage_cyls();
      walls();
    }
    buttons();
    led();
  }
}

frame();
