import numpy as np 
from contrast import Contrast

class main(Contrast):

    def __init__(self, layers, incident_light):
        self.layers = layers
        self.incident_light = incident_light

        self.disulfuro = np.loadtxt("./refractive_indexes/disulfuro_molibdeno.txt", delimiter='\t')  # Disulfuro wavelength and refractive index
        self.silicon = np.loadtxt("./refractive_indexes/silicon.txt", delimiter='\t')             # Silicon wavelength and refractive index

        self.disulfuro_n = self.disulfuro[:,1] - 1j*self.disulfuro[:,2];        # Disulfuro refractive index
        self.silicon_n = self.silicon[:,1] + 1j*self.silicon[:,2];              # Silicon refractive index
        self.air_n = 1.0 + 0j                                                   # Air refractive index

    def silicon_dioxide_n(self, wavelength):
        n = 4.7996E-18*wavelength**6 - 1.9105E-14*wavelength**5 + 3.1531E-11*wavelength**4 - 2.7757E-08*wavelength**3 + 1.3872E-05*wavelength**2 - 3.8045E-03*wavelength + 1.9176
        return n

    def blood_n(self, wavelength):
        # From 400 to 750 nm in lenght light
        A1 = 0.7960 
        A2 = 5.1819e-6 
        B1 = 1.0772e4
        B2 = -7.8301e5 # Sellmaeier coeficients
        n = 1 + ((A1*wavelength**2)/(wavelength**2 - B1))+(A2*wavelength**2)/(wavelength**2 - B2)
        n = np.sqrt(n)
        return n

    def glass_n(self, wavelength):
        n = (-3.9079E-15*wavelength**5 + 1.2309E-11*wavelength**4 - 1.5542E-08*wavelength**3 + 9.9180E-06*wavelength**2 - 3.2596E-03*wavelength + 1.9673) + 0j #extrapoleted from [2]
        return n

    def grafeno(self):
        wavelength = self.silicon[:,0]
        graphene_n = 2.6-1.3j                                                           # Graphene refractive index
        silicon_dioxide_n = self.silicon_dioxide_n(wavelength)

        graphene_thickness = [0.34]
        silicon_dioxide_thickenss = np.linspace(0,350,30)
        silicon_dioxide_samples_thickness = np.linspace(0,350,5)                         # Samples of thicknes to linear plot

        contrast = Contrast(self.layers, silicon_dioxide_samples_thickness, wavelength, self.incident_light)
        contrast.refractive_indexes(self.air_n, graphene_n, silicon_dioxide_n, self.silicon_n)
        contrast.layers_thickness(graphene_thickness, silicon_dioxide_thickenss)

        contrast.thicknes_l1_variation("graphene", "SiO_2")

    def disulfuro_molibdeno(self):
        wavelength = self.disulfuro[:,0]
        disulfuro_molibdeno_n = self.disulfuro_n
        silicon_dioxide_n = self.silicon_dioxide_n(wavelength)

        disulfuro_molibdeno_thickness = [0.55, 0.60]
        silicon_dioxide_thickness = np.linspace(0,350,30)
        silicon_dioxide_samples_thickness = np.linspace(0,350,5)                         # Samples of thicknes to linear plot

        contrast = Contrast(self.layers, silicon_dioxide_samples_thickness, wavelength, self.incident_light)
        contrast.refractive_indexes(self.air_n, disulfuro_molibdeno_n, silicon_dioxide_n, self.silicon_n)
        contrast.layers_thickness(disulfuro_molibdeno_thickness, silicon_dioxide_thickness)

        contrast.thicknes_l1_variation("disulfuro_molibdeno", "SiO_2")

    def glass_blood(self):
        wavelength = np.linspace(400,700,50)
        blood_n = self.blood_n(wavelength)
        glass_n = self.glass_n(wavelength)

        glass_thickness = [140000]
        blood_thickness =np.arange(2000, 5000, 50).tolist()
        blood_samples_thickness = np.arange(2000, 5000, 500).tolist()                                     # Samples of thicknes to linear plot

        contrast = Contrast(self.layers, blood_samples_thickness, wavelength, self.incident_light)
        contrast.refractive_indexes(self.air_n, glass_n, blood_n, glass_n)
        contrast.layers_thickness(glass_thickness, blood_thickness)

        contrast.thicknes_l1_variation("glass_blood", "Sangre")

    def oil_glass_blood(self):
        wavelength = np.linspace(400,700,50)
        oil_n = 1.516
        blood_n = self.blood_n(wavelength)
        glass_n = self.glass_n(wavelength)

        blood_thickness = np.arange(2000, 5000, 50).tolist()
        glass_thickness = [140000]
        oil_thickness = np.arange(200, 500, 50).tolist()
        blood_samples_thickness = np.arange(2000, 5000, 1000).tolist()                                   # Samples of thicknes to linear plot

        contrast = Contrast(self.layers, blood_samples_thickness, wavelength, self.incident_light)
        contrast.refractive_indexes_glass(self.air_n, oil_n, glass_n, blood_n, glass_n)
        contrast.layers_thickness(oil_thickness, blood_thickness)

        contrast.thicknes_l1_variation_glass("oil_glass_blood", glass_thickness, "Sangre")

if __name__ == "__main__":

    layers = 3                                      # Number of layers, it does not include air
    incident_light = 0                              # 1 up and 0 down light incident

    main_class = main(layers, incident_light)       # 

    # Graphene
    #main_class.grafeno()

    # Disulfuro Molibdeno
    #main_class.disulfuro_molibdeno()

    # glass_blood
    main_class.glass_blood()

    layers = 4                                      # Number of layers, it does not include air
    incident_light = 0                              # 1 up and 0 down light incident

    main_class = main(layers, incident_light)       # 

    # oil_glass_blood
    main_class.oil_glass_blood()

