// -----------------------------------------------------------------------------
// 3D-Model (OpenSCAD): holder for Lipo-Amigo-Pro.
//
// The holder will be glued to the support.
//
// Author: Bernhard Bablok
// License: GPL3
//
// https://github.com/bablokb/circuitpython-clock
//
// -----------------------------------------------------------------------------

include <dimensions.scad>
include <BOSL2/std.scad>

x_pcb = 23;
y_pcb = 35;
z_pcb =  2.0;                                  // including some SMD-parts

x_holder = x_pcb + 2*w2 + 2*gap;
y_holder = y_pcb + 2*w2 + 2*gap;
b_holder = 1.8;                                // base thickness
z_holder = b_holder + z_pcb;

prism_x = 5;                                 // prism size
prism_z = 0.6;

x_usbc = 9;                                    // cutout usb-c connector
x_pins = 3;
y_pins = 26;
x_bat  = 18;

module prism() {
  translate([-x_holder/2+prism_x/4,-y_holder/2+prism_x/2,z_holder+prism_z/2])
    xrot(-90) 
      prismoid(size1=[prism_x,prism_z], size2=[0,prism_z], shift=[-prism_x/2,0], h=prism_x,anchor=CENTER);
}

module holder() {
  difference() {
    union() {
      cuboid([x_holder,y_holder,b_holder],anchor=BOTTOM+CENTER);
      rect_tube(size=[x_holder,y_holder],wall=w2,h=z_holder,
                                          anchor=BOTTOM+CENTER);
    }
    translate([0,-y_holder/2-w2,b_holder-fuzz]) cuboid([x_usbc,4*w2,z_holder],anchor=BOTTOM+CENTER);
    translate([x_pcb/2-x_pins/2,0,-fuzz]) cuboid([x_pins,y_pins,b_holder+2*fuzz],anchor=BOTTOM+CENTER);
    translate([-x_pcb/2+x_bat/2-gap,y_holder/2+w2,b_holder-fuzz]) cuboid([x_bat,4*w2,z_holder],anchor=BOTTOM+CENTER);
  }
  prism();
  xflip() prism();
}

holder();
