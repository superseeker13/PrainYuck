#  Copyright 2019 Edward Conn <cardseller2@gmail.com>

#require 'pycall/import'
#include PyCall::Import
#eval = PyCall.import_module('bfparser')

Shoes.app title: "PrainYuck-IDE", :width => 400, :height => 140 do
    self.stack do
        flow :width => 400 do
            @prgbox = edit_box title: "Code"
            @input = edit_line title: "Input"
        end
        
        flow :width => 400 do
            button "Lint" do
                append { para "Good to go." }
            end
            button "Run" do
                append { eval.eval("#{@prgbox.text}") }
            end
        end
    end
end
