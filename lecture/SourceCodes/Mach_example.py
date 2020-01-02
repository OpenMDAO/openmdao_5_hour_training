class MachExternalCodeComp(om.ExternalCodeImplicitComp):

    def initialize(self):
        self.options.declare('super_sonic', types=bool)

    def setup(self):
        self.add_input('area_ratio', val=1.0, units=None)
        self.add_output('mach', val=1., units=None)
        self.declare_partials(of='mach', wrt='area_ratio', method='fd')

        self.input_file = 'mach_input.dat'
        self.output_file = 'mach_output.dat'

        # providing these are optional; the component will verify that any input
        # files exist before execution and that the output files exist after.
        self.options['external_input_files'] = [self.input_file]
        self.options['external_output_files'] = [self.output_file]

        self.options['command_apply'] = [
            sys.executable, 'extcode_mach.py', self.input_file, self.output_file,
        ]
        self.options['command_solve'] = [
            sys.executable, 'extcode_mach.py', self.input_file, self.output_file,
        ]

    def apply_nonlinear(self, inputs, outputs, residuals):
        with open(self.input_file, 'w') as input_file:
            input_file.write('residuals\n')
            input_file.write('{}\n'.format(inputs['area_ratio'][0]))
            input_file.write('{}\n'.format(outputs['mach'][0]))

        # the parent apply_nonlinear function actually runs the external code
        super(MachExternalCodeComp, self).apply_nonlinear(inputs, outputs, residuals)

        # parse the output file from the external code and set the value of mach
        with open(self.output_file, 'r') as output_file:
            mach = float(output_file.read())
        residuals['mach'] = mach

    def solve_nonlinear(self, inputs, outputs):
        with open(self.input_file, 'w') as input_file:
            input_file.write('outputs\n')
            input_file.write('{}\n'.format(inputs['area_ratio'][0]))
            input_file.write('{}\n'.format(self.options['super_sonic']))
        # the parent apply_nonlinear function actually runs the external code
        super(MachExternalCodeComp, self).solve_nonlinear(inputs, outputs)

        # parse the output file from the external code and set the value of mach
        with open(self.output_file, 'r') as output_file:
            mach = float(output_file.read())
        outputs['mach'] = mach