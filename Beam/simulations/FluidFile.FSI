under Problem {
  Type   = UnsteadyAeroelastic;
  Mode   = Dimensional;
  Framework = Embedded;
}

under AdaptiveMeshRefinement {
  
 under SelectionCriterion[0] {
    Type = WallProximity;
    under WallProximityCriterion {
      OuterZone_d = 1.0;
      OuterZone_H = 0.4;
      InnerZone_D = 2.0e-2;
      InnerZone_H = 4.0e-3;
      DeltaPlus = 1.0;
      EdgeLengthMinMaxRatio = 0.4;
    }
    MinimumEdgeLength = 4e-3;
    NumLevels = 10;
    PreRefine = On;
  }

 
  under SelectionCriterion[1] {
      Type = Hessian;
      under HessianCriterion {
      SensorType = Velocity;
      Threshold = 1.0e-1;
       HessianConstruction = LeastSquares;
       CoarseningThreshold = 2.0e-2;
    }
    PreRefine = Off;
    MinimumEdgeLength = 1.5e-2;
    NumLevels = 1;
  }

 under RefinementDomain {
      Type = Sphere;
      under Sphere {
      	    Center_x = 0.0;
            Center_y = 0.0;
            Center_z = 30.00;
            Radius = 45;
      }
  }

  Mode = NonDimensional; 
  RecomputeWallDistance = 2;  
  BisectionStrategy = Isotropic;
  MaximumRefinementIterations = 1000;
  Eps = 1e-3;
  MaximumCoarseningIterations = 1000;
  BalancingFrequency = 50;
  ItrFactor = 1000.0;
  UseUnsteadyStrategy = 1;
  Frequency = 50;
}

under Input {
  GeometryPrefix = "references.Unsteady/fluidmodel";
  Matcher = "../data/fluidmodel.match.fluid";
  EmbeddedSurface = "../sources/embeddedSurface.top";
 
  // Restart from Unsteady simulation
  // Edit Restart.data, delete everything except the MaxNodePreAMR
  
  Solution = "references.Unsteady/Solution.bin";
  RestartData = "references.Unsteady/Restart.data";

}
                                                                                                 
under Output {
  under Postpro {
    PostprocessSides = 1;
    Prefix   = "results.FSI/";
    Mach  = "Mach.bin";
    EmbeddedSurfaceDisplacement = "../postpro.FSI/EmbeddedSurfaceDisplacement.xpost";
    LiftandDrag  = "../postpro.FSI/LiftandDrag.out";
    Frequency = 1000;
  }
  under Restart {
    Prefix = "references.FSI/"; 
    Solution = "Solution.bin";
    RestartData = "Restart.data";
    Position = "Position.data";
    EmbeddedPosition = "EmbeddedPosition.data";
    Frequency = 1000;
  }
}

under Equations {
  Type = NavierStokes;
  under FluidModel[0] {
    Fluid = PerfectGas;
    under GasModel {
      SpecificHeatRatio = 1.4;
      IdealGasConstant = 287.0;
    }
  }
  under ViscosityModel {
    Type = Sutherland;
  }
  under TurbulenceClosure {
    Type = LESModel;
    under LESModel{
      Type = Vreman;
      under Vreman {
        Cs = 0.07;
      }
      Delta = Volume;
    }
  }
}


under BoundaryConditions {
  under Inlet {
    Type    = External;
    Mach    = 0.5;
    Density = 0.58;
    Pressure = 40000;
    Alpha   = 0.0;
    Beta    = 0.0;
  }
  under Wall {
    Type        = Adiabatic;
    Integration = Full;
  }  
}

under Space {
  under NavierStokes {
    Flux              = Roe;
    Reconstruction    = Linear;
    AdvectiveOperator = FiniteVolume;
    Limiter           = VanAlbada;
    Gradient          = LeastSquares;
    Beta              = 0.3333333333333333;
    Gamma             = 1.0;
  }
  under Boundaries {
    Type = StegerWarming;
  }
}



under Time {
  Type = Implicit;
  MaxIts = 500000;
  MaxTime = 0.2;
  under CflLaw{
      Strategy = Fixed;
      Cfl0 = 10.0;
      CflMax = 10.0;
 }
  under Implicit {
    Type = RungeKutta2;
    MatrixVectorProduct = FiniteDifference;
    TurbulenceModelCoupling = Weak;
    under Newton {
      MaxIts = 5;
      Eps = 0.001;
      FailSafe = AlwaysOn;
      under LinearSolver {
        under NavierStokes {
          Type = Gmres;
          MaxIts = 150;
          KrylovVectors = 150;
          Eps = 0.01;
          under Preconditioner {
            Type = Ras;
            Fill = 0;
          }
        }
        under TurbulenceModel {
          Type = Gmres;
          MaxIts = 50;
          KrylovVectors = 50;
          Eps = 0.01;
          under Preconditioner {
            Type = Ras;
            Fill = 0;
          }
        }
      }
    }
  }
}


under EmbeddedFramework {
  TypeHalfRiemannProblem = Surrogate;
  RiemannNormal = Structure;
}
