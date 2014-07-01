"""

module __FickianDiffusion__
===============================================================================

"""

import scipy as sp
from .__LinearSolver__ import LinearSolver

class FickianDiffusion(LinearSolver):
    r'''
    '''

    def __init__(self,**kwargs):
        r'''
        '''
        super(FickianDiffusion,self).__init__(**kwargs)
        self._logger.info('Create '+self.__class__.__name__+' Object')
        
    def setup(self,fluid,conductance='diffusive_conductance',quantity='mole_fraction',**params):
        r'''
        '''  
        self._logger.info("Setup "+self.__class__.__name__)   
        super(FickianDiffusion,self).setup(fluid=fluid,conductance=conductance,quantity=quantity)
        
    def calc_eff_diffusivity(self, clean=False):
        D_normal = self._calc_eff_prop()
        self._eff_property = D_normal/self._fluid['pore.molar_density']
        return self._eff_property
        



