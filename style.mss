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

#sqlitetest {
  	polygon-fill: pink;
    [type="residential"] {
    	polygon-fill: blue;
    }
}

#pointtest {
  marker-width: 3;
  marker-fill: #f00;
  text-name: "[name]";
  text-allow-overlap: true;
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
    }
    ::rightpath {
      line-width: 1;
      line-offset: -8;
      line-color: #ccc;
      
      [sidewalk_right="yes"] {
        line-width: 2;
        line-color: #222;
      }
    }
  }
  [highway="footway"] {
    line-width: 2;
    line-color: #222;
    line-smooth: 1;
  }
  [highway!="footway"] {
    ::inside {
      line-width: 13;
      line-color: #ddd;
      line-cap: round;

      [interesting_to_peds="no"] {
	    line-color: #fff;
      }
        
      [on_bus_route="yes"] {
        ::busroute {
          line-width: 14;
          line-color:#fdd6a4;
          line-cap: round;
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
      }
    }
  }
}
