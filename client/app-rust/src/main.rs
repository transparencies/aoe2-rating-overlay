#![windows_subsystem = "windows"]

// use web_view::*;
use neutrino::{App, Window};
use neutrino::widgets::label::Label;
use neutrino::widgets::button::Button;

#[macro_use]
extern crate clap;
use clap::App as OtherApp;

// mod download;

fn main() {
    let yaml = load_yaml!("../cli.yml");
    let matches = OtherApp::from_yaml(yaml).get_matches();

    // web_view::builder()
    //     .title("")
    //     .content(Content::Html(HTML))
    //     .size(300, 70)
    //     .frameless(false)
    //     .debug(true)
    //     .user_data("")
    //     .invoke_handler(|webview, arg| {
    //         match arg {
    //             "exit" => webview.exit(),
    //             _ => (),
    //         }
    //         Ok(())
    //     })
    //     .run()
    //     .unwrap();

let mut label = Label::new("my_label");
label.set_text(&("Your Steam-ID is: ".to_owned() + matches.value_of("steamid").unwrap()));

let mut button = Button::new("my_button");
button.set_text("Exit");


let mut window = Window::new();
window.set_title("aoe2overlay");
window.set_size(300,70);
// window.set_frameless();
window.set_debug();

// window.set_child(Box::new(label));
window.set_child(Box::new(button));

App::run(window);


// TODO: remember last used steamid (parse from file) 

}

// const HTML: &str = r#"
// <!doctype html>
// <html>
//   <body>
//         <object data="../assets/overlay.svg" type="image/svg+xml"></object>
//         <button onclick="external.invoke('exit')" style="display:block;width:80px;height:15px;font-size:12pt;margin:25px auto;">exit</button>
//   </body>
// </html>
// "#;