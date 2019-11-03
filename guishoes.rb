#  Copyright 2019 Edward Conn <cardseller2@gmail.com>
#  

Shoes.app title: "PrainYuck-IDE", :width => 400, :height => 140 do
    self.stack do
        edit_box "Code" 
        flow :width => 400 do
            button "Lint" do
                append { para "Good to go." }
            end
            button "Run" do
                append { para "Running." }
            end
        end
    end
end
