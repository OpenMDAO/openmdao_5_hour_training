# build the model
prob = Problem()
indeps = prob.model.add_subsystem('indeps', IndepVarComp(), promotes=['*'])
indeps.add_output('a', .5)
indeps.add_output('Area', 10.0, units='m**2')
indeps.add_output('rho', 1.225, units='kg/m**3')
indeps.add_output('Vu', 10.0, units='m/s')

prob.model.add_subsystem('a_disk', ActuatorDisc(),
                        promotes_inputs=['a', 'Area', 'rho', 'Vu'])

# setup the optimization
prob.driver = ScipyOptimizeDriver()
prob.driver.options['optimizer'] = 'SLSQP'

prob.model.add_design_var('a', lower=0., upper=1.)
prob.model.add_design_var('Area', lower=0., upper=1.)
prob.model.add_constraint('a_disk.Ct', lower=0, upper=0.8)
# negative one so we maximize the objective
prob.model.add_objective('a_disk.Cp', scaler=-1)
prob.model.approx_totals(method='fd')
prob.setup()
prob.run_driver()