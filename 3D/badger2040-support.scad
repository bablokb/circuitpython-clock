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

y_corpus_bot   = y1_panel/3;
y_corpus_top   = y_corpus_bot*2/3;
y_corpus_shift = (y_corpus_bot-y_corpus_top)/2;
h_corpus       = z_body + 20;

// --- the corpus   ------------------------------------------------------------

module corpus() {
  rect_tube(size1=[x1_panel,y_corpus_bot],size2=[x1_panel,y_corpus_top],
                   h=h_corpus,wall=w4,shift=[0,-y_corpus_shift],
                   rounding=r_panel,irounding=r_panel,anchor=BOTTOM+CENTER);
  // workaround: prusa-slice does not slice the first layer correctly, so add some supprt
  cuboid([x1_panel,y_corpus_bot/3,0.2],
          chamfer=y_corpus_bot/6,edges="Z",anchor=BOTTOM+CENTER);
  cuboid([x1_panel/10,y_corpus_bot,0.2],
          chamfer=x1_panel/20,edges="Z",anchor=BOTTOM+CENTER);

}

// --- fase   ----------------------------------------------------------------

module fase() {
  translate([0,y_conn/2,0])
    prismoid(size1=[x_bcon,y_bcon],size2=[x_conn,0],shift=[0,-y_conn/2],h=y_conn,
             spin=180,orient=FRONT+FORWARD,anchor=BOTTOM+FRONT);
}

// --- base-connectors   -----------------------------------------------------

module connectors() {
  translate([-x1_panel/2+x1_panel/8,
             -y_corpus_bot/2-y_bcon/2+fuzz,z_bcon_off]) {
       cuboid([x_bcon-gap,y_bcon,z_bcon-y_bcon],anchor=BOTTOM+CENTER);
       fase();
  }
  translate([+x1_panel/2-x1_panel/8,
             -y_corpus_bot/2-y_bcon/2+fuzz,z_bcon_off]) {
       cuboid([x_bcon-gap,y_bcon,z_bcon-y_bcon],anchor=BOTTOM+CENTER);
       fase();
  }
}

// --- cutouts   -------------------------------------------------------------

module cutouts() {
  // cable hole
  translate([+1.5*x_cable,-(y_corpus_bot/2-w4/2)-fuzz,(z_body-z_cable)/2])
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
