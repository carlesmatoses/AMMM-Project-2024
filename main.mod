main {
  for (var i = 1; i <= 8; i++) {
    writeln("Starting iteration " + i);
    var dataFile = "project." + i + ".dat";
    var src = new IloOplModelSource("project.mod");
    var def = new IloOplModelDefinition(src);
    var cplex = new IloCplex();
    var model = new IloOplModel(def,cplex);
    var data = new IloOplDataSource(dataFile);
    model.addDataSource(data);
    model.generate();
    
    cplex.epgap=0.01;
    if (cplex.solve()) {
      
      var com_size = 0;
      for (var p = 1; p <= model.D; p++) com_size += model.n[p];
      var sol = 0;
      for (var i = 1; i <= model.N; i++) {
        for (var j = i + 1; j <= model.N; j++) {
          if (model.x[i][j] == 1) {
            writeln(i + " " + j + " " + model.m[i][j]);
            sol +=  model.m[i][j];
          }
        }
      }
      writeln(com_size);
      sol /= (com_size*(com_size - 1)/2); 
      writeln(sol);
  
      writeln("Objective " + (cplex.getObjValue() - com_size)/(com_size*(com_size - 1)) + "%");
      
      var commission = "";
      for (var i = 1; i <= model.N; i++) {
        if (model.c[i] == 1) commission += " " + i; 
      }
      writeln("Commission:" + commission);
    }
    else {
      writeln("Not solution found");
    }
    
    model.end();
    data.end();
    cplex.end();
    def.end();
    src.end();
    
    writeln("finish");
  }
};