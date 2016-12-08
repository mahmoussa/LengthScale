from config import options as O
from tools import openRootFileR, closeRootFile, plotName, plotPath, \
                  drawSignature
from ROOT import TCanvas, gStyle, TPad, gPad, TLine

def plotPerBxStep(options):
    """Save histograms (per BX and step) to PDF files"""
    name = options['scan'] + '_' + options['name'] + options['extra']
    f = openRootFileR(name)
    crossings = O['crossings']
    if options['combine']:
        crossings.append('all')
    for bx in crossings:
        for step in range(len(O['nominalPos'][options['scan']])):
            histname = plotName(options['scan']+'_'+options['name']+ \
                                options['extra']+'_bx'+str(bx)+'_step'+ \
                                str(step), timestamp=False)
            filename = plotPath(options['scan']+'_'+options['name']+ \
                                options['extra']+'_bx'+str(bx)+'_step'+ \
                                str(step), timestamp=True)
            print '<<< Save plot:', filename
            hist = f.Get(histname)
            canvas = TCanvas()
            canvas.SetLogx(options['logx'])
            canvas.SetLogy(options['logy'])
            gStyle.SetOptStat(options['optstat'])
            gStyle.SetOptFit(options['optfit'])
            hist.Draw()
            hist.GetXaxis().SetTitle(options['xtitle'])
            hist.GetXaxis().SetRangeUser(options['xmin'], options['xmax'])
            hist.GetYaxis().SetTitle(options['ytitle'])
            drawSignature(histname)
            canvas.Print(filename)
            canvas.Close()
    closeRootFile(f, name)

def numberClusterPerBxStep(scan, combine=False):
    """Save cluster number histograms to PDF files"""
    options = {'name': 'nCluster', 'scan': scan, 'xmin': -0.5, 'xmax': 5000.5, \
               'logx': 0, 'logy': 1, 'xtitle': 'Number of Pixel Clusters (per event)', \
               'ytitle': 'Number of Events', 'optstat': 101110, 'optfit': 0, \
               'extra': '', 'combine': combine}
    plotPerBxStep(options)

def numberVerticesPerBxStep(scan, combine=False):
    """Save vertex number histograms to PDF files"""
    options = {'name': 'nVtx', 'scan': scan, 'xmin': -0.5, 'xmax': 6.5, 'logx': 0, \
               'logy': 1, 'xtitle': 'Number of Vertices (per event)', \
               'ytitle': 'Number of Events', 'optstat': 1110, 'optfit': 0, \
               'extra': '', 'combine': combine}
    plotPerBxStep(options)

def vertexPositionPerBxStep(scan, fit='', combine=False):
    """Save vertex position histograms to PDF files"""
    options = {'name': 'vtxPos', 'scan': scan, 'xmin': -1e3, 'xmax':3e3, \
               'logx': 0, 'logy': 0, 'xtitle': 'Measured Vertex Position [#mum]', \
               'ytitle': 'Number of Events','optstat': 1110, 'optfit': 101,
               'extra': fit, 'combine': combine}
    plotPerBxStep(options)

def plotPerDirectionBx(options):
    """Save directional fit plots (per BX) to PDF files"""
    name = options['scan'] + '_'+ options['name'] + options['fitted'] \
           + '_collected'
    f = openRootFileR(name)
    for bx in O['crossings']:
        plotname = plotName(name+'_bx'+str(bx), timestamp=False)
        filename = plotName(name+'_bx'+str(bx), timestamp=True)
        filepath = plotPath(name+'_bx'+str(bx), timestamp=True)
        print '<<< Save plot:', filename
        graphs = f.Get(plotname)
        residuals = f.Get(plotname+'_residuals')
        
        gStyle.SetOptFit(options['optfit'])
        canvas = TCanvas()
        canvas.cd()
        pad1 = TPad('pad1', 'pad1', 0, 0.3, 1, 1)
        pad2 = TPad('pad2', 'pad2', 0, 0, 1, 0.3)
        pad1.Draw()
        pad2.Draw()
        
        pad1.cd()
        gPad.SetMargin(0.1, 0.01, 0.0, 0.3)
        graphs.Draw('AP')
        gPad.Update()
        for j, graph in enumerate(graphs.GetListOfGraphs()):
            graph.SetMarkerStyle(21)
            graph.SetMarkerColor(2+2*j)
            stats = graph.GetListOfFunctions().FindObject('stats')
            stats.SetTextColor(2+2*j)
            stats.SetX1NDC(0.1+0.5*j)
            stats.SetX2NDC(0.40+0.5*j)
            stats.SetY1NDC(0.72)
            stats.SetY2NDC(0.88)
            graph.GetFunction(options['fit']).SetLineColor(2+2*j)
        graphs.GetYaxis().SetTitle(options['ytitle'])
        
        pad2.cd()
        gPad.SetMargin(0.1, 0.01, 0.3, 0.0)
        for j, residual in enumerate(residuals.GetListOfGraphs()):
            residual.SetMarkerStyle(21)
            residual.SetMarkerColor(2+2*j)
        residuals.Draw("AP")
        residuals.GetXaxis().SetTitle('Nominal Position [#mum]')
        residuals.GetYaxis().SetTitle('Residuals')
        residuals.GetXaxis().SetTitleOffset(3)
        residuals.GetXaxis().SetLabelOffset(0.02)
        residuals.GetYaxis().SetNdivisions(305)
        gPad.Update()
        line = TLine(pad2.GetUxmin(), 0.0, pad2.GetUxmax(), 0.0)
        line.SetLineColor(14)
        line.SetLineStyle(3)
        line.Draw()
        
        for axis in [graphs.GetYaxis(), residuals.GetXaxis(), \
                     residuals.GetYaxis()]:
            axis.SetTitleFont(133)
            axis.SetTitleSize(16)
            axis.SetLabelFont(133)
            axis.SetLabelSize(12)
            axis.CenterTitle()
        
        for pad in [pad1, pad2]:
            pad.Modified()
            pad.Update()
        
        canvas.cd()
        drawSignature(filename)
        canvas.Print(filepath)
        canvas.Close()
    closeRootFile(f, name)

def vertexPositionPerDirectionBx(scan, fitted='', combine=False):
    """Save vertex position directional plots to PDF files"""
    options = {'name': 'vtxPos', 'scan': scan, 'fitted': fitted, 'optfit': 111, \
               'fit': 'pol1', 'ytitle': 'Measured Vertex Position [#mum]', \
               'combine': combine}
    plotPerDirectionBx(options)