import numpy as np 
import matplotlib.pyplot as plt
#from mpl_toolkits.axes_grid1.inset_locator import inset_axes

class Graphics():

    def __init__(self, wavelength, layers_name, layer_l2_name):
        self.fig = plt.figure(figsize=(16,6)); 
        self.wavelength = wavelength
        self.layers_name = layers_name
        self.layer_l2_name = layer_l2_name

    def linear_plot(self, contrast, thicknes_l2) -> None:
        self.fig.add_subplot(1, 2, 1); 
        wavelength = self.wavelength
        plt.grid(True)

        for i in range (0,len(thicknes_l2)):  
            if thicknes_l2[i]>=1000:
                plt.plot(wavelength, contrast[i],"-",linewidth=3,label="$d_{2}= $"+str(thicknes_l2[i]/1000)+" $\mu m$") # plot contrast vs wavelength

            else:
                plt.plot(wavelength, contrast[i],"-",linewidth=3,label="$d_{2}= $"+str(thicknes_l2[i])+" $nm$") # plot contrast vs wavelength 

            plt.legend(loc="best",fontsize=10)
            plt.tick_params(labelsize=12)
            plt.xlabel("Longitud de Onda [nm]",fontsize=16)
            plt.ylabel("Contraste",fontsize=16)

    def contour_plot(self, contrast, thicknes_l1_i, thicknes_l2) -> None:
        self.fig.add_subplot(1, 2, 2)

        contrast = np.transpose(contrast)
        wavelength = self.wavelength

        plt.contourf(thicknes_l2, wavelength, contrast, 100, cmap='jet')     
        plt.tick_params(labelsize=12)
        plt.xlabel("Espesor de $\mathregular{"+self.layer_l2_name+"}$ [nm]",fontsize=16)
        plt.ylabel("Longitud de Onda [nm]",fontsize=16)
        plt.ylim(min(wavelength),max(wavelength)); 
        #cbaxes = inset_axes(ax, width="20%", height="3%", loc=1) 
        #plt.colorbar(cax=cbaxes, ticks=[float("{0:.3f}".format(np.min(contrast))), 0], orientation='horizontal')
        cb = plt.colorbar()
        cb.set_label(label='Contraste', size=16)
        #plt.suptitle( "images/" +self.layer_name + "_" + str(thicknes_l1_i)+" nm$ \;\;\;\; ", fontsize=18,y=0.96)
        plt.grid(True)
        plt.savefig( "images/" +self.layers_name + "/" + str(thicknes_l1_i)+".jpg", transparent=True, bbox_inches='tight',dpi=300)
        plt.close()