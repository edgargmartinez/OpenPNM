import openpnm as op
import scipy as sp
from numpy.testing import assert_allclose


class DispersionTest:

    def setup_class(self):
        sp.random.seed(0)
        self.net = op.network.Cubic(shape=[4, 3, 1], spacing=1.0)
        self.geo = op.geometry.GenericGeometry(network=self.net,
                                               pores=self.net.Ps,
                                               throats=self.net.Ts)

        self.phase = op.phases.GenericPhase(network=self.net)
        self.phys = op.physics.GenericPhysics(network=self.net,
                                              phase=self.phase,
                                              geometry=self.geo)
        self.phys['throat.diffusive_conductance'] = 1e-15
        self.phys['throat.hydraulic_conductance'] = 1e-15

        sf = op.algorithms.StokesFlow(network=self.net, phase=self.phase)
        sf.setup(quantity='pore.pressure',
                 conductance='throat.hydraulic_conductance')
        sf.set_value_BC(pores=self.net.pores('back'), values=1)
        sf.set_value_BC(pores=self.net.pores('front'), values=0)
        sf.run()
        self.phase.update(sf.results())

    def test_dispersion(self):
        ad = op.algorithms.Dispersion(network=self.net, phase=self.phase)
        ad.setup(quantity='pore.concentration',
                 diffusive_conductance='throat.diffusive_conductance',
                 hydraulic_conductance='throat.hydraulic_conductance',
                 pressure='pore.pressure')
        ad.set_value_BC(pores=self.net.pores('back'), values=2)
        ad.set_value_BC(pores=self.net.pores('front'), values=0)
        ad.run()

        x = [0., 0., 0.,
             0.89688173, 0.89688173, 0.89688173,
             1.53952557, 1.53952557, 1.53952557,
             2., 2., 2.]
        y = ad[ad.settings['quantity']]
        assert_allclose(actual=y, desired=x)

    def test_outflow_BC(self):
        ad = op.algorithms.Dispersion(network=self.net, phase=self.phase)
        ad.setup(quantity='pore.concentration',
                 diffusive_conductance='throat.diffusive_conductance',
                 hydraulic_conductance='throat.hydraulic_conductance',
                 pressure='pore.pressure')
        ad.set_value_BC(pores=self.net.pores('back'), values=2)
        ad.set_outflow_BC(pores=self.net.pores('front'))
        ad.run()

        y = ad[ad.settings['quantity']].mean()
        assert_allclose(actual=y, desired=2)

    def teardown_class(self):
        ws = op.Workspace()
        ws.clear()


if __name__ == '__main__':

    t = DispersionTest()
    t.setup_class()
    for item in t.__dir__():
        if item.startswith('test'):
            print('running test: '+item)
            t.__getattribute__(item)()
    self = t
