// -----------------------------------------------------------------------------
// 3D-Model (OpenSCAD) for a Badger2040.
//
// This model is the back cover with a holder for the AHT20 temp/hum sensor.
//
// Author: Bernhard Bablok
// License: GPL3
//
// https://github.com/bablokb/circuitpython-clock
//
// -----------------------------------------------------------------------------

include <dimensions.scad>
include <BOSL2/std.scad>

x_sensor     = 3.4;
y_sensor     = 3.4;
y_sensor_off = 1.27;

y_stemma     = 8;
z_stemma     = 3.1;
z_pcb        = 1.6;

x_aht20      = 25.4  + gap;
y_aht20      = 17.98 + gap;
z_aht20      = z_pcb + z_stemma;

// --- the base plate with cutouts   -------------------------------------------

module plate() {
  difference() {
    cuboid([x1_panel,y1_panel,z_panel],
            rounding=r_panel, anchor=BOTTOM+CENTER,
            edges="Z");
    // cutout for sensor
    translate([0,y_sensor_off,-fuzz]) 
      cuboid([x_sensor,y_sensor,z_panel+2*fuzz], anchor=BOTTOM+CENTER);
  }
}

// --- aht20   -----------------------------------------------------------------

module aht20() {
  translate([0,0,z_panel-fuzz]) {
    difference() {
      // wall around AHT20
      rect_tube(size=[x_aht20+2*w2,y_aht20+2*w2],wall=w2,h=z_aht20,
                      anchor=BOTTOM+CENTER);
      // cutouts for Stemma/Qt
      translate([-x_aht20/2-w2/2-fuzz,0,0])
          cuboid([w2+2*fuzz,y_stemma,z_aht20+fuzz],anchor=BOTTOM+CENTER);
      translate([+x_aht20/2+w2/2-fuzz,0,0]) 
          cuboid([w2+2*fuzz,y_stemma,z_aht20+fuzz],anchor=BOTTOM+CENTER);
    }
    // wall around sensor
    translate([0,y_sensor_off,0])
         rect_tube(size=[x_sensor+2*w2,y_sensor+2*w2],wall=w2,h=z_stemma+2*fuzz,
                   anchor=BOTTOM+CENTER);
  }
}

// --- walls   -----------------------------------------------------------------

module walls() {
  translate([0,0,z_panel-fuzz]) difference() {
    cuboid([x_wall,y_wall,z_wall],
            rounding=r_panel, anchor=BOTTOM+CENTER,
            edges="Z");
    cuboid([x_wall-2*w2,y_wall-2*w2,z_wall+2*fuzz],
            rounding=r_panel, anchor=BOTTOM+CENTER,
            edges="Z");
  }
}

// --- final cover   -----------------------------------------------------------

module cover() {
  difference() {
    union() {
      plate();
      aht20();
      walls();
    }
  }
}

cover();
//plate();
//aht20();
//walls();