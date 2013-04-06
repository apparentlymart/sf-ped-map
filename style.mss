Map {
  background-color: #b8dee6;
}

#countries {
  ::outline {
    line-color: #85c5d3;
    line-width: 2;
    line-join: round;
  }
  polygon-fill: #eee;
}

#landuse {
  line-width: 2;
  polygon-opacity:0;
  line-opacity: 0;
  [landuse="construction"] {
    polygon-fill:#b6b591;
    line-color:#a6a581;
    polygon-opacity:1;
    line-opacity: 1;
  }
  [landuse="retail"] {
    polygon-fill:#f0dad9;
    line-color:#e0cac9;
    polygon-opacity:1;
    line-opacity: 1;
  }
  [landuse="park"] {
    polygon-fill:#daf0d9;
    line-color:#cae0c9;
    polygon-opacity:1;
    line-opacity: 1;
  }
  [landuse="parking"] {
    polygon-fill:#fff;
    line-color:#ccc;
    polygon-opacity:1;
    line-opacity: 1;
  }
}

#buildings {
  line-color:#bcaeac;
  line-width:2;
  polygon-opacity:1;
  polygon-fill:#ccbebc;
  ::label[zoom>=19] {
    text-placement: interior;
    text-name: "[name]";
    text-face-name: "Arial Regular";
    text-size: 12;
    text-wrap-width: 10;
    text-fill: #7c6e6c;
    text-halo-fill: #ccbebc;
    text-halo-radius: 5;
  }
}

#highways {
  [highway!="footway"] {
    ::leftpath {
      line-width: 1;
      line-offset: 8;
      line-color: #ccc;

      [sidewalk_left="yes"] {
        line-width: 2;
        line-color: #222;
      }
      [highway="cycleway"] {
        line-offset: 4;
      }
      [highway="service"] {
        line-offset: 4;
      }
      [highway="residential"] {
        line-offset: 6;
      }
    }
    ::rightpath {
      line-width: 1;
      line-offset: -8;
      line-color: #ccc;
      
      [sidewalk_right="yes"] {
        line-width: 2;
        line-color: #222;
      }
      [highway="cycleway"] {
        line-offset: -4;
      }
      [highway="service"] {
        line-offset: -4;
      }
      [highway="residential"] {
        line-offset: -6;
      }
    }
  }
  [highway="footway"] {
    line-width: 2;
    line-color: #222;
    line-smooth: 1;

    ::footlabel {
      text-placement: line;
      text-name: "[name]";
      text-face-name: "Arial Regular";
      text-size: 12;
      text-avoid-edges: true;
      text-halo-fill: #eeeeee;
      text-halo-radius: 5;
    }
  }
  [highway!="footway"] {
    ::inside {
      line-width: 13;
      line-color: #ddd;
      line-cap: round;

      [highway="cycleway"] {
        line-width: 7;
      }
      [highway="service"] {
        line-width: 7;
      }
      [highway="residential"] {
        line-width: 10;
      }
      
      [interesting_to_peds="no"] {
	    line-color: #fff;
      }
        
      [on_bus_route="yes"] {
        ::busroute {
          line-width: 14;
          line-color:#fdd6a4;
          line-cap: round;
          [highway="residential"] {
            line-width: 10;
          }
        }
      }
    }
    ::label {
      [interesting_to_peds="yes"] {
        text-placement: line;
        text-name: "[name]";
        text-face-name: "Arial Regular";
        text-size: 12;
        text-avoid-edges: true;
        [highway="cycleway"] {
          text-size: 8;
        }
        [highway="service"] {
          text-size: 8;
        }
        [highway="residential"] {
          text-size: 10;
        }
      }
    }
  }
}

