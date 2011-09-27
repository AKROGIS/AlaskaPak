using System.Collections.Generic;
using System.Linq;
using System.Windows.Forms;
using ESRI.ArcGIS.Carto;
using ESRI.ArcGIS.esriSystem;
using NPS.AKRO.ArcGIS.Forms;
using NPS.AKRO.ArcGIS.Common;

namespace NPS.AKRO.ArcGIS
{
    public class CopyRasterSymbology : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        private AlaskaPak _controller;
        private CopyRasterSymbologyForm _form;
        private List<NamedLayer> _rasterLayers;

        //Enabled is defined in the Button base class and defaults to True.
        //This button cannot set its Enabled state until after it is instantiated by the user.
        //This occurs when the user clicks it for the first time in the UI (remember it defaulted to Enabled).
        //In addition to being instantiated, the new object gets the OnClick event.
        //Once this button is instantiated, it can maintain the state of Enabled which will
        //enable/disable the UI (and subsequent OnClick events).
        //We maintain the state of Enabled by monitoring ArcMap events.
        //We do not overrider the OnUpdate() method because the Enabled state is always current.

        public CopyRasterSymbology()
        {
            AlaskaPak.RunProtected(GetType(), MyConstructor);
        }

        private void MyConstructor()
        {
            _controller = AlaskaPak.Controller;
            _controller.LayersChanged += Controller_LayersChanged;
            _rasterLayers = _controller.GetRasterLayers();
            Enabled = MapHasTwoOrMoreRasterLayers;
        }

        protected override void OnClick()
        {
            AlaskaPak.RunProtected(GetType(), MyClick);
        }

        private void MyClick()
        {
            if (Enabled)
            {
                if (_form != null) //User may click when form is already loaded.
                {
                    _form.Activate();
                }
                else
                {
                    _form = new CopyRasterSymbologyForm();
                    _form.CopyRasterEvent += Form_Copy;
                    _form.FormClosed += Form_Closed;
                    LoadFormList();
                    _form.Show();
                }
            }
            else
            {
                MessageBox.Show(@"You must have two or more raster layers in your map to use this command.",
                                @"For this command...", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
        }

        private bool MapHasTwoOrMoreRasterLayers
        {
            get { return _rasterLayers.Count > 1; }
        }

        private void LoadFormList()
        {
            _form.LoadLists(_rasterLayers.Select(rl => rl.Name));
        }

        #region Event Handlers

        //What we will do when the controller says the layers have changed
        private void Controller_LayersChanged()
        {
            _rasterLayers = _controller.GetRasterLayers();
            Enabled = MapHasTwoOrMoreRasterLayers;
            if (_form != null)
                LoadFormList();
        }

        //What we will do when the form says it has closed
        internal void Form_Closed(object sender, FormClosedEventArgs e)
        {
            _form = null;
        }

        //What we will do when the form says it has layers to copy
        internal void Form_Copy(object sender, CopyRasterEventArgs e)
        {
            Copy(e.Source, e.Targets);
            _form.Close();
        }

        #endregion

        #region Helper Functions (Tool Specific Logic)

        private void Copy(int sourceLayerIndex, IEnumerable<int> targetLayerIndices)
        {
            var sourceLayer = _rasterLayers[sourceLayerIndex].Layer as IRasterLayer;
            //Debug.Assert(sourceLayer != null, "Source layer not found");
            if (sourceLayer != null)
            {
                IObjectCopy objectCopier = new ObjectCopyClass();
                IRasterRenderer sourceRender = sourceLayer.Renderer;
                //Debug.Assert(sourceRender != null, "Source layer has no renderer");
                if (sourceRender != null)
                {
                    foreach (int index in targetLayerIndices)
                    {
                        var destLayer = _rasterLayers[index].Layer as IRasterLayer;
                        //Debug.Assert(destLayer != null, "Destination layer not found");
                        if (destLayer != null)
                            //destLayer.Renderer = sourceRender;  //layers share the same renderer
                            destLayer.Renderer = (IRasterRenderer)objectCopier.Copy(sourceRender);
                    }
                }
            }
            ArcMap.Document.UpdateContents();
            ArcMap.Document.ActiveView.Refresh();
        }

        #endregion
    }
}
