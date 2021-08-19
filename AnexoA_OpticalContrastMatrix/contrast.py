import numpy as np 
from graphics import Graphics

class Contrast(Graphics):

    def __init__(self, layers, samples_thickness_l2, wavelength, incident_light):
        self.layers = layers
        self.wavelength = wavelength
        self.incident_light = incident_light
        self.samples_thickness_l2 = samples_thickness_l2

    def refractive_indexes(self, layer_n0, layer_n1, layer_n2, layer_n3) -> None:
        self.layers_n = np.array([layer_n0, layer_n1, layer_n2, layer_n3], dtype = object)          # Refractives indexes of layers including air
        self.layers_n_0 = np.array([layer_n0, layer_n0, layer_n2, layer_n3], dtype = object)        # Refractives indexes with layer_n1 equal to layer_n0

    def refractive_indexes_glass(self, layer_n0, layer_n1, layer_n2, layer_n3, layer_n4) -> None:
        self.layers_n = np.array([layer_n0, layer_n1, layer_n2, layer_n3, layer_n4], dtype = object)          # Refractives indexes of layers including air
        self.layers_n_0 = np.array([layer_n0, layer_n0, layer_n0, layer_n3, layer_n4], dtype = object)        # Refractives indexes with layer_n1 equal to layer_n0

    def layers_thickness(self, thicknes_l1, thicknes_l2) -> None:
        self.thicknes_l1 = thicknes_l1
        self.thicknes_l2 = thicknes_l2

    def matriz_M(self, n, d):
        '''
        Here is generated the M 2x2 matrix wich depends of
        refractive index, width of layers and wavelength

        Parameters:
        n, vector with refractive index of each layer
        d, vector with width of layers

        Response:
        M, result of matricial product by Mm and Em by layer
        '''
        
        N = self.layers
        wavelength = self.wavelength

        M = np.array([[1, 0],[0, 1]], dtype = object)

        for m in range(1, N):
            r = (n[m - 1] - n[m])/(n[m - 1] + n[m])
            phi = (2 * np.pi * n[m] * d[m - 1])/wavelength
            Mm = np.array([[1, r], [r, 1]], dtype=object)

            Em = np.array([[np.exp(1j*phi), 0], [0, np.exp(-1j*phi)]], dtype = object)
            M = np.dot(M, np.dot(Mm, Em))

        r = (n[N - 1] - n[N])/(n[N - 1] + n[N])
        Mm = np.array([[1, r], [r, 1]], dtype = object)
        M = np.dot(M, Mm)

        return M
    
    def intensity(self, n, d):
        '''
        Here is calculated the intensity from result of matrix M 
        taking present side of inciden of light

        Parameters:
        n, vector with refractive index of each layer
        d, vector with width of layers

        Response:
        I, is the value of intensity
        '''

        incident_light = self.incident_light

        side = np.array([[incident_light], [not incident_light]])
        M = self.matriz_M(n, d)
        out = np.dot(M, side)
        I = abs(out[1]/out[0])**2

        return I

    def contrast(self, d, d_1):
        '''
        Here is calculated the constrast 
        
        '''

        layers_n = self.layers_n
        layers_n_0 = self.layers_n_0

        I_1 = self.intensity(layers_n_0, d_1)
        I = self.intensity(layers_n, d)
        C = (I - I_1)/(I + I_1)

        return C[0]

    def thicknes_l2_variation(self, thicknes_l1_i, thicknes_l2):

        contrast_graph_data = []

        for thicknes_l2_i in thicknes_l2:

            d = np.array([thicknes_l1_i, thicknes_l2_i])
            d_1 = np.array([0, thicknes_l2_i])
            C = self.contrast(d, d_1)
            
            contrast_graph_data.append(C)

        return contrast_graph_data

    def thicknes_l1_variation(self, layers_name, layer_l2_name) -> None:

        thicknes_l1 = self.thicknes_l1
        samples_thickness_l2 = self.samples_thickness_l2
        thicknes_l2 = self.thicknes_l2

        for thicknes_l1_i in thicknes_l1:

            plot = Graphics(self.wavelength, layers_name, layer_l2_name); 
            
            contrast = self.thicknes_l2_variation(thicknes_l1_i, samples_thickness_l2)
            plot.linear_plot(contrast, samples_thickness_l2)

            contrast = self.thicknes_l2_variation(thicknes_l1_i, thicknes_l2)
            plot.contour_plot(contrast, thicknes_l1_i, thicknes_l2)

    def thicknes_l2_variation_glass(self, thicknes_l1_i, glass_thickness,thicknes_l2):

        contrast_graph_data = []

        for thicknes_l2_i in thicknes_l2:

            d = np.array([thicknes_l1_i, glass_thickness, thicknes_l2_i], dtype = object)
            d_1 = np.array([0, 0, thicknes_l2_i])
            C = self.contrast(d, d_1)
            
            contrast_graph_data.append(C)

        return contrast_graph_data

    def thicknes_l1_variation_glass(self, layers_name, glass_thickness, layer_l2_name) -> None:

        thicknes_l1 = self.thicknes_l1
        samples_thickness_l2 = self.samples_thickness_l2
        thicknes_l2 = self.thicknes_l2

        for thicknes_l1_i in thicknes_l1:

            plot = Graphics(self.wavelength, layers_name, layer_l2_name); 
            
            contrast = self.thicknes_l2_variation_glass(thicknes_l1_i, glass_thickness,samples_thickness_l2)
            plot.linear_plot(contrast, samples_thickness_l2)

            contrast = self.thicknes_l2_variation_glass(thicknes_l1_i, glass_thickness,thicknes_l2)
            plot.contour_plot(contrast, thicknes_l1_i, thicknes_l2)