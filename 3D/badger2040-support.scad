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

// --- the corpus   ------------------------------------------------------------

module corpus() {
  rect_tube(size1=[x1_panel,y1_panel/2],size2=[x1_panel,y1_panel/3],
                   h=z_body,wall=w4,shift=[0,-1/12*y1_panel],
                   rounding=r_panel,irounding=r_panel,anchor=BOTTOM+CENTER);
}

// --- fase   ----------------------------------------------------------------

module fase() {
  prismoid(size1=[w4,w4],size2=[w4,0],shift=[0,-w4/2],h=w4,
           spin=180,orient=FRONT+FORWARD,anchor=BOTTOM+FRONT);
}

// --- base-connectors   -----------------------------------------------------

module connectors() {
  translate([-x1_panel/2+x1_panel/8,
             -y1_panel/4+fuzz,z_bcon_off+w4]) {
       cuboid([w4,2*w4,z_bcon-w4],anchor=BOTTOM+CENTER);
       fase();
  }
  translate([+x1_panel/2-x1_panel/8,
             -y1_panel/4+fuzz,z_bcon_off+w4]) {
       cuboid([w4+gap/2,2*w4,z_bcon-w4],anchor=BOTTOM+CENTER);
       fase();
  }
}

// --- cutouts   -------------------------------------------------------------

module cutouts() {
  // cable hole
  translate([+1.5*x_cable,-y1_panel/4+w4/2-fuzz,(z_body-z_cable)/2])
       cuboid([x_cable,w4+2*fuzz,z_cable],anchor=BOTTOM+CENTER);
  
}

// --- final model   ---------------------------------------------------------

module support() {
  difference() {
    union() {
      corpus();
      connectors();
    }
    cutouts();
  }
}

support();
