using System;
using Gtk;
using System.Collections.Generic;
using System.IO;
using Gdk;

namespace viewer2
{
	class MainClass
	{
		public static Dictionary<string, Param> paramdict;
		public static Dictionary<ParamSet, string> directories;
		public static MainWindow win;
		public static TreeView trv;
		public static TreeStore trs;
		public static Container drawingArea;
		public static Widget currentImage;
		public static VBox[] vboxes = new VBox[3];
		public static SpinButton spin_button = null;//new SpinButton(0.0, 100000000.0, 1.0);
		public static Dictionary<ParamSet, int> params_to_number = new Dictionary<ParamSet, int>();
		public static Dictionary<int, ParamSet> number_to_params = new Dictionary<int, ParamSet>();
		public static int max_plots = 0;
		public static void Main (string[] args)
		{
			Application.Init ();
			
			string brpath = "symulacje";
			if(!Directory.Exists(brpath))
				brpath = "simulations";
			
			if(!Directory.Exists(brpath))
				brpath = ".";
			
			
			
			Console.WriteLine("Please wait while the simulations are being scanned...");
			
			DirectoryInfo di = new DirectoryInfo(brpath);
			
			
			DirectoryInfo[] di2 = di.GetDirectories("batch-run*");
/*			foreach(DirectoryInfo dil in di2)
			{
				Console.WriteLine(dil.FullName);
			}*/
			List<DirectoryInfo> di3 = new List<DirectoryInfo>();
			
			foreach(DirectoryInfo dil in di2)
			{
				if(File.Exists(System.IO.Path.Combine(dil.FullName, "params.txt")))
				   di3.Add(dil);
			};
			di2 = di3.ToArray();
			
			if(di2.Length == 0)
			{
				MessageDialog md = new MessageDialog(new MainWindow(), 
				                                     DialogFlags.DestroyWithParent,
				                                     MessageType.Error,
				                                     ButtonsType.Close, 
				                                     "Simulation pack not found. Please unzip it into simulations/ directory.");
				
//				Application.Init();
				md.Run();
				md.Destroy();
				Environment.Exit(0);
			}
			
			Param.GetNames(System.IO.Path.Combine(di2[0].FullName, "params.txt"));
			paramdict = new Dictionary<string, Param>();
	
			foreach(DirectoryInfo dil in di2)
			{
				int i=1; 
				while(File.Exists(System.IO.Path.Combine(dil.FullName, "plot-" + i.ToString() + ".png")))
					i++;
				if(i>max_plots)
					max_plots = i;
			};
			
			win = new MainWindow ();
			HBox mhbox = new HBox();
			HBox hbox = new HBox();
	//		spin_button = new SpinButton(0.0, 100000000.0, 1.0);
			
			for(int i=0; i<3; i++)
			{
				vboxes[i] = new VBox();
				hbox.Add(vboxes[i]);
			}
		
			mhbox.Add(hbox);
			
			uint hpos = 0;
			uint vpos = 0;
			foreach(string pp in Param.paramnames)
			{
				if(hpos == 3)
				{
					vpos += 1;
					hpos = 0;
				}
				Param nparam = new Param(pp, vboxes[hpos], hpos, vpos);
				paramdict[pp] = nparam;
				hpos += 1;
			};
			
			directories = new Dictionary<ParamSet, string>();
			
			
			int sims_count = 0;
			foreach(DirectoryInfo dil in di2)
			{
	//			Console.WriteLine(dil.FullName);
				ParamSet ps = new ParamSet(System.IO.Path.Combine(dil.FullName, "params.txt"));
				foreach(KeyValuePair<string, string> kvp in ps.dict)
				{
	//				Console.WriteLine(kvp.Key + "	" + kvp.Value);
					paramdict[kvp.Key].AddValue(kvp.Value);
				}
				
				try{
					directories.Add(ps, dil.FullName);
				}
				catch(System.ArgumentException)
				{
					Console.WriteLine("Parameter conflict:");
					Console.WriteLine(ps.ToString() + " -> " + dil.FullName);
					Console.WriteLine(ps.ToString() + " -> " + directories[ps]);
					throw;
				}
				
				int run_number = GetNumberFromPath(dil.Name);
				number_to_params[run_number] = ps;
				params_to_number[ps] = run_number;
				sims_count++;
			
			}
			spin_button = new SpinButton(0.0, (float) sims_count-1, 1.0);
			
			foreach(KeyValuePair<string, Param> kvp in paramdict)
			{
				kvp.Value.SelectFirst();
			}
			
			
/*			Button button = new Button("Pokaż");
			button.Clicked += new EventHandler(ButtonClicked);
			hbox.Attach(button, 1, 2, 8, 9);
*/		
			
	//		win.Add(mhbox);
//			Param p = new Param("par1", hbox);
//			Param p = paramdict[0];
/*			p.AddValue("3");
			p.AddValue("lllllllllllll");
			p.AddValue("3");
			 */
/*			Param r = new Param("par2", hbox);
			r.AddValue("fffff");
			r.AddValue("we");
				*/
			
			Frame fr = new Frame("Plot number");
			trv = new TreeView();
			trs = new TreeStore(typeof(string));
			trv.Model = trs;
			trv.AppendColumn("value", new CellRendererText(), "text", 0);
			trv.HeadersVisible = false;
			for(int i=1; i<max_plots; i++)
			{
				trs.AppendValues(i.ToString());
			}
			
			fr.Add(trv);
			vboxes[1].Add(fr);
			TreeIter tri;
			
			trs.GetIterFirst(out tri);
			trv.Selection.SelectIter(tri);
			
			trv.CursorChanged += ButtonClicked;
			
			Table tbl2 = new Table(3, 3, false);
			mhbox.Add(tbl2);
			drawingArea = new VBox();
			tbl2.Attach(drawingArea, 1, 2, 1, 2);
			currentImage = new Label(" ");
			drawingArea.Add(currentImage);
			
			/* Setup for spin button at top */
			
			HBox sp_hbox = new HBox();
			Label run_num_label = new Label("Run number:");
			run_num_label.SetAlignment(0.9f, 0.0f);
			sp_hbox.Add(run_num_label);
			sp_hbox.Add(spin_button);
			
			Button spin_but_go = new Button("Go");
			spin_but_go.Clicked += SpinbuttonChanged;
			sp_hbox.Add(spin_but_go);
			
			
			
			VBox top_sp_vb = new VBox();
			
			top_sp_vb.Add(sp_hbox);
			top_sp_vb.Add(mhbox);
				
			win.Add(top_sp_vb);
			win.ShowAll ();
			ButtonClicked(null, null);
			Application.Run ();
		}

		static void HandleSpin_buttonChanged (object sender, EventArgs e)
		{
			
		}
		
		public static ParamSet GetSelection()
		{
			Dictionary<string, string> d = new Dictionary<string, string>(); 
			foreach(KeyValuePair<string, Param> kvp in paramdict)
			{
				d.Add(kvp.Key, kvp.Value.GetSelected());
			}
			return new ParamSet(d);
		}
		
		public static void ButtonClicked(object obj, EventArgs args)
		{
			ParamSet s = GetSelection();
	/*		foreach(KeyValuePair<string, string> kvp in s.dict)
			{
	//			Console.WriteLine(kvp.Key + "	" + kvp.Value);
			}
	*/		currentImage.Destroy();
			if(directories.ContainsKey(s))
			{
	//			Console.WriteLine(directories[s]);
				TreeIter iter;
				TreeModel model;
			
				TreeSelection ts = trv.Selection;
			
				ts.GetSelected(out model, out iter);
				string val = (string) model.GetValue(iter, 0);
				string ds = directories[s];
				string path = System.IO.Path.Combine(ds, "plot-" + val + ".png");
				MainWindow.instance.Title = ds;
//				Window win2 = new Window("Wykres " + path);
//				win2.DeleteEvent += KillWindow;
//				Pixbuf pb = new Pixbuf(path);
//				Pixbuf pb = new Pixbuf();
//				pb = pb.ScaleSimple(pb.Width/2, pb.Height/2, InterpType.Bilinear);
				currentImage = new Gtk.Image(path);
				
			}
			else
			{
//				Dialog d = new Dialog("", win, DialogFlags.DestroyWithParent);
//				d.AddButton("OK", ResponseType.Close);
//				d.VBox.Add(new Label("Brak wykresu."));
//				Console.WriteLine("FALSE");
//				d.ShowAll();
//				d.Run();
//				d.Destroy();
				currentImage = new Label("Plot unavailable for chosen parameters");
			}
			drawingArea.Add(currentImage);
			drawingArea.ShowAll();
			if(params_to_number.ContainsKey(s))
				spin_button.Text = params_to_number[s].ToString();
		}
		
		public static void KillWindow(object o, DeleteEventArgs e)
		{
			///gtk.window.destroy()
		}
		
		public static int GetNumberFromPath(string path)
		{
			string[] path_split = path.Split('-');
			return int.Parse(path_split[path_split.Length-1]);
		}
			
		
		public static void SpinbuttonChanged(object sender, EventArgs e)
		{
			int run_no = spin_button.ValueAsInt;
			ParamSet ps = number_to_params[run_no];
			foreach(KeyValuePair<string, Param> kvp in paramdict)
			{
				kvp.Value.SelectFromParamSet(ps);
			}
			ButtonClicked(null, null);
		}
		
		
	}
	
	class Param
	{
		public static List<string> paramnames;
		public static Tooltips tooltips = null;
		private string name;
		List<string> paramvalues;
		private VBox container;
		private Frame frame;
//		private VBox vbox;
		TreeStore treestore;
		TreeView treeview;
		private Dictionary<string, TreeIter> val_to_iter = new Dictionary<string, TreeIter>();
		private string Shorten(string s)
		{
			if(s.Length < 13)
				return s;
			else
				return s.Substring(0,10)+"...";
		}
		public Param(string pname, VBox _container, uint hpos, uint vpos)
		{
			if(tooltips == null)
				tooltips = new Tooltips();
			name = pname;
			container = _container;
			
			frame = new Frame(Shorten(pname));
			tooltips.SetTip(frame, pname, pname);
			
//			vbox = new VBox(false, 10);
//			container.Attach(frame, hpos, hpos+1, vpos, vpos+1);
			container.Add(frame);
//			vbox.Add(new Label(name));
			
			treestore = new TreeStore(typeof(string));
			treeview = new TreeView();
			treeview.Model = treestore;
			treeview.AppendColumn("value", new CellRendererText(), "text", 0);
			treeview.HeadersVisible = false;
			
			frame.Add(treeview);
			
			paramvalues = new List<string>();
		}
		
		public void AddValue(string val)
		{
			if(!paramvalues.Contains(val))
			{
				paramvalues.Add(val);
				val_to_iter[val] = treestore.AppendValues(val);
			}
		}
		
		public string GetSelected()
		{
			TreeIter iter;
			TreeModel model;
			
			TreeSelection ts = treeview.Selection;
			
			ts.GetSelected(out model, out iter);
			string val = (string) model.GetValue(iter, 0);
			return val;
		}
		
		public void SelectFirst()
		{
			TreeIter iter;
			treestore.GetIterFirst(out iter);
			treeview.Selection.SelectIter(iter);
			treeview.CursorChanged += MainClass.ButtonClicked;
		}
		
		public void SelectFromParamSet(ParamSet ps)
		{
			treeview.Selection.SelectIter(val_to_iter[ps.dict[name]]);
		}
		
		public static string[] hidden_names = {}; /*"number_of_mutations", "fitness_use_relative", "initial_phenotype_stdev", "deletion_probability", "duplicative_transposition_probability", 
											   "min_survival_fitness", "no_phenotype_properties", "is_drift_directed", "stability_period", "niche_size", "transposon_creation_rate",
											   "fitness_pressure", "nonlethal_transposition_likelihood", "fluctuations_magnitude", "transposition_mutation_stdev", "inactivation_probability",
											   "random_pressure", "expected_mutation_shift", "deauton_probability"};*/
		
		public static bool IsNameHidden(string name)
		{
			foreach(string hn in hidden_names)
				if(hn == name)
					return true;
			return false;
		}
		
		public static void GetNames(string filename)
		{
			paramnames = new List<string>();
			StreamReader sr = new StreamReader(filename);
			while(!sr.EndOfStream)
			{
				string line = sr.ReadLine();
				string name = line.Split(' ')[0];
				if(!IsNameHidden(name))
					paramnames.Add(name);
			}
			sr.Close();
		}
	}
	class ParamSet : IEquatable<ParamSet>
	{
		
/*		public static bool is_allowed(string name)
		{
			foreach(string s in allowed_fields)
				if(s == name)
					return true;
			return false;
		}*/
		
		public Dictionary<string, string> dict;
		
		public override int GetHashCode ()
		{
			string s = "";
			foreach(KeyValuePair<string, string> kvp in dict)
			{
				s += kvp.Value;
			}
			return s.GetHashCode();
		}
		
		public bool Equals(ParamSet other)
		{
			foreach(string pname in Param.paramnames)
				if(dict[pname] != other.dict[pname])
				{
	//				Console.WriteLine(pname + "	" + dict[pname] + "	" + other.dict[pname]);
					return false;
				}
			return true;
		}
		public ParamSet(string filename)
		{
			dict = new Dictionary<string, string>();
			StreamReader sr = new StreamReader(filename);
			
			while(!sr.EndOfStream)
			{
				string line = sr.ReadLine();
				string[] sarr = line.Split(' ');
				if(!Param.IsNameHidden(sarr[0]))
				{
					dict.Add(sarr[0], sarr[4]);
				}
			}
			sr.Close();
		}
		public ParamSet(Dictionary<string, string> dictionary)
		{
			dict = dictionary;
		}
	}
	class ModelRun
	{
		ParamSet paramset;
		string path;
		
		public ModelRun(string dirpath)
		{
			path = dirpath;
			paramset = new ParamSet(path + "/" + "par.txt");
		}
	}		
}

