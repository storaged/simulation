using System;
using Gtk;

public class MainWindow : Gtk.Window
{
	public static MainWindow instance = null;
	public MainWindow () : base(Gtk.WindowType.Toplevel)
	{
		this.DeleteEvent += OnDeleteEvent;
		instance = this;
	}

	// Quit the app when the user clicks on the window close button
	protected void OnDeleteEvent (object sender, DeleteEventArgs a)
	{
		Application.Quit ();
		a.RetVal = true;
	}
}

