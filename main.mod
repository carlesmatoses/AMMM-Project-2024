main {
    var dataFile = "project.1.dat";
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
  
      var num_pairs = com_size*(com_size - 1)/2;
      writeln("Objective " + cplex.getObjValue()/num_pairs);
      
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
};