// -----------------------------------------------------------------------------
// 3D-Model (OpenSCAD) for a Badger2040.
//
// This model is the front cover for the support with cutouts for a button
// and a LED (connected to Amigo-Lipo-Pro).
//
// Author: Bernhard Bablok
// License: GPL3
//
// https://github.com/bablokb/circuitpython-clock
//
// -----------------------------------------------------------------------------

include <dimensions.scad>
include <BOSL2/std.scad>

x_pcb = 36 + 2*gap;
y_pcb = 10 + 2*gap;
h_pcb = 1.6;
a_pcb = 1.6;

x_co_led     = 1.6 + 2*gap;
y_co_led     = 4.2 + 2*gap;
x_co_led_off = -8.19;
y_co_led_off = 0;

x_co_pins       = 5.1 + 2*gap;
y_co_pins       = x_co_pins;
h_co_pins       = 0.4;
x_co_pins_off   = 1.38;    // relative to pcb
y_co_pins_off   = -1.81;   // relative to pcb

x_co_btn        = 6.3;
y_co_btn        = x_co_btn;
x_co_btn2       = 6.7;
y_co_btn2       = 7.2;
h_co_btn2       = 0.4;
x_co_btn_off    = 8.21;
y_co_btn_off    = 0;

d_pcb_cyl = 2.5 - 2*gap;
x_pcb_cyl_off = 14.87;
y_pcb_cyl_off = 0;

x_cutout     = 18.4;
y_cutout     = 11;
h_cutout     = 2.6;

// --- holder for button/led-pcb   -----------------------------------------------------

module pcb_holder() {
  difference() {
    // body of pcb-holder
    cuboid([x_pcb+2*w2,y_pcb+2*w2,z_panel],anchor=BOTTOM+CENTER);
    // minus LED-cutout
    translate([x_co_led_off,y_co_led_off,-fuzz])
       cuboid([x_co_led,y_co_led,z_panel+2*fuzz],anchor=BOTTOM+CENTER);
    // minus pin-cutout
    translate([x_co_pins_off,y_co_pins_off,h_co_pins])
       cuboid([x_co_pins,y_co_pins,z_panel+2*fuzz],anchor=BOTTOM+CENTER);
    // minus button-cutout
    translate([x_co_btn_off,y_co_btn_off,-fuzz])
       cuboid([x_co_btn,y_co_btn,z_panel+2*fuzz],anchor=BOTTOM+CENTER);
    translate([x_co_btn_off,y_co_btn_off,h_co_btn2])
       cuboid([x_co_btn2,y_co_btn2,z_panel+2*fuzz],anchor=BOTTOM+CENTER);
  }
  // walls above pcb-holder
  translate([0,0,z_panel-fuzz])
     rect_tube(isize=[x_pcb,y_pcb],h=h_pcb+a_pcb,wall=w2,anchor=BOTTOM+CENTER);
  // two cylinders for mounting-holes
  translate([-x_pcb_cyl_off,y_pcb_cyl_off,z_panel-fuzz])
     cylinder(d=d_pcb_cyl,h=h_pcb+a_pcb,anchor=BOTTOM+CENTER);
  translate([+x_pcb_cyl_off,y_pcb_cyl_off,z_panel-fuzz])
     cylinder(d=d_pcb_cyl,h=h_pcb+a_pcb,anchor=BOTTOM+CENTER);
}

// --- cover for button/led-pcb   ----------------------------------------------

module pcb_cover() {
   difference() {
    // body of pcb-cover
    cuboid([x_pcb,y_pcb,a_pcb],anchor=BOTTOM+CENTER);
    // minus LED-cutout
    translate([x_co_led_off,y_co_led_off,-fuzz])
       cuboid([x_co_led,y_co_led,a_pcb+2*fuzz],anchor=BOTTOM+CENTER);
    // minus pin-cutout
    translate([x_co_pins_off,y_co_pins_off,-fuzz])
       cuboid([x_co_pins,y_co_pins,a_pcb+2*fuzz],anchor=BOTTOM+CENTER);
    // minus button-cutout
    translate([x_co_btn_off,y_co_btn_off,-fuzz])
       cuboid([x_co_btn2,y_co_btn2,a_pcb+2*fuzz],anchor=BOTTOM+CENTER);
    // minus cylinder-cutouts
    translate([-x_pcb_cyl_off,y_pcb_cyl_off,-fuzz])
       cylinder(d=d_pcb_cyl,h=a_pcb+2*fuzz,anchor=BOTTOM+CENTER);
    translate([+x_pcb_cyl_off,y_pcb_cyl_off,-fuzz])
       cylinder(d=d_pcb_cyl,h=a_pcb+2*fuzz,anchor=BOTTOM+CENTER);
  } 
}

// --- the base plate with cutouts   -------------------------------------------

module plate() {
  x_holder_off = -x_wall/2+w4+x_pcb/2+w2;
  difference() {
    cuboid([x1_panel,y_support_bot,z_panel],
            rounding=r_panel, anchor=BOTTOM+CENTER,
            edges="Z");
    // cutout for pcb-holder
    translate([x_holder_off,0,0]) cuboid([x_pcb+2*w2-fuzz,y_pcb+2*w2-fuzz,z_panel],anchor=BOTTOM+CENTER);;
  }
  // pcb-holder
  translate([x_holder_off,0,0]) zrot(180) pcb_holder();
}

// --- walls   -----------------------------------------------------------------

module walls() {
  y_wall_bot = y_support_bot - 2*w4 - gap;
  y_wall_top = y_support_top - 2*w4 - gap;
  translate([0,0,z_panel-fuzz])
    difference() {
      // create a full-height tube (to get the slanted side correct)
      rect_tube(size1=[x_wall,y_wall_bot],size2=[x_wall,y_wall_top],
                       h=h_support,wall=w4,shift=[0,-y_support_shift],
                       rounding=r_panel,irounding=0,anchor=BOTTOM+CENTER);
      // and remove the part above z_wall
      translate([0,0,z_wall]) cuboid([x1_panel,y1_panel,h_support],
                                      anchor=BOTTOM+CENTER);
  }
}

// --- final cover   -----------------------------------------------------------

module cover() {
  plate();
  walls();
}

cover();
//pcb_holder();
//translate([0,0,20]) pcb_cover();