//
// Created by nourisaj on 1/6/20.
//

#pragma once
#include "fl/Headers.h"
#include <iostream>
#include <string>
#include <map>
#include <memory>
#include <algorithm>
#include <filesystem>
#include <functional>
#include <cassert>
using namespace fl;
using namespace std;

// auto SELECTIVE_CHECK = [&](){
//     vector<string> target_input = {"CD"};
//     vector<string> target_output = {"Mo"};
//     // map<string,double> non_target_inputs = { {"CD",0.5},{"AE",0}};
//     map<string,double> non_target_inputs = { {"Mg",0.5},{"AE",0}};
//     unsigned steps = 10;
//     std::function<void(unsigned)> RECURSIVE = [&](unsigned int j){
//         for (unsigned i = 0; i < steps; i++) {
//             auto input_tag  = target_input[target_input.size()-j];
//             engine->getInputVariable(input_tag)->setValue(engine->getInputVariable(input_tag)->getMinimum() +
//                     i * (engine->getInputVariable(input_tag)->range() / steps));
//             if (j > 1){        
//                 RECURSIVE(j -1); 
//             }
//             else{
//                 for (auto &non_target:non_target_inputs){
//                     auto tag = non_target.first;
//                     auto value = non_target.second;
//                     // cout<<tag<<" "<<value<<endl;
//                     engine->getInputVariable(tag)->setValue(value);
//                 }
//                 engine->process();
//                 for (auto &input_tag:target_input){
//                     cout<<setw(4)<< input_tag << ": "<<setw(4)<<engine->getInputVariable(input_tag)->getValue() <<" ";
//                 }

//                 for (auto &output_tag:target_output){
//                     cout<<setw(4)<<output_tag <<": "<<setw(4)<<Op::str(engine->getOutputVariable(output_tag)->getValue())<<" ";
//                 }

//                 cout<<endl;

//             }

//         };
//     };
//     RECURSIVE(target_input.size());
// };


vector<string> generate_rules(vector<vector<string>> factors, vector<string> levels, string target);
struct base_exception{
    base_exception(std::string msg):message(msg){

    }
    std::string message;
    const char *what() const throw() {
        return message.c_str();
    }
};
struct invalid_fuzzy_definition: public base_exception{
    invalid_fuzzy_definition(std::string msg):base_exception(msg){}
    
};
struct invalid_fuzzy_output: public base_exception{
    invalid_fuzzy_output(std::string msg):base_exception(msg){}
};
struct invalid_fuzzy_input: public base_exception{
    invalid_fuzzy_input(std::string msg):base_exception(msg){}
};
struct invalid_engine: public base_exception{
    invalid_engine(std::string msg):base_exception(msg){}
};
struct undefined_param_key: public base_exception{
    undefined_param_key(std::string msg):base_exception(msg){}
};
using myMap = std::map<string,float>;

struct base_model{
    // base_model(){

    // };
    
    base_model(myMap &params_):params(params_){
        // this->antecedents = {}
        // this->consequents = {}
        this->default_inputs = {};
    };
    virtual void define_consequents(){
        // early Diff: 6 levels
        auto OUTPUT_EARLYDIFF = [&]() {
            vector<float> intervals = {0,this->params["early_diff_L"],.5,this->params["early_diff_H"],this->params["early_diff_VH"], 1};
            vector<string> terms = {"Z", "L", "M", "H", "VH", "EH"};
            OutputVariable* out = new OutputVariable;
            out->setName("early_diff");
            out->setDescription("");
            out->setEnabled(true);
            out->setRange(0.000, 1);
            out->setLockValueInRange(false);
            out->setAggregation(fl::null);
            out->setDefuzzifier(new WeightedAverage("Automatic"));
            out->setDefaultValue(fl::nan);
            out->setLockPreviousValue(false);
            for (unsigned i=0; i < terms.size(); i ++){
                out->addTerm(new Constant(terms[i], intervals[i]));
            }
            this->engine->addOutputVariable(out);
        };
        OUTPUT_EARLYDIFF();
        this->output_tags.push_back("early_diff");

        // late Diff: 5 levels
        auto OUTPUT_LATEDIFF = [&]() {
            vector<float> intervals = {0,this->params["late_diff_L"],.5,this->params["late_diff_H"], 1};
            vector<string> terms = {"Z", "L", "M", "H", "VH"};
            OutputVariable* out = new OutputVariable;
            out->setName("late_diff");
            out->setDescription("");
            out->setEnabled(true);
            out->setRange(0.000, 1);
            out->setLockValueInRange(false);
            out->setAggregation(fl::null);
            out->setDefuzzifier(new WeightedAverage("Automatic"));
            out->setDefaultValue(fl::nan);
            out->setLockPreviousValue(false);
            for (unsigned i=0; i < terms.size(); i ++){
                out->addTerm(new Constant(terms[i], intervals[i]));
            }
            this->engine->addOutputVariable(out);
        };
        OUTPUT_LATEDIFF();
        this->output_tags.push_back("late_diff");
    }

    myMap forward(myMap & inputs_){
        std::string status;
        if (not this->engine->isReady(&status)) {
            cout<<"ERROR: engine is not ready"<<endl;
            throw invalid_engine("[engine error] engine is not ready:n" + status);
        };

        for (auto &input:inputs_){ // send in the inputs
            if (std::find(this->input_tags.begin(), this->input_tags.end(), input.first) == this->input_tags.end()){
                cout<<"ERROR: The input variable '"+ input.first+"' is not defined is the controller"<<endl;
                throw invalid_fuzzy_input("The input variable '"+ input.first+"' is not defined is the controller");
            }
            // cout<< input.first<<" "<<   input.second<<endl;
            this->engine->getInputVariable(input.first)->setValue(input.second);
            
        }
        this->engine->process();
        myMap outputs;
        for (auto &tag:this->output_tags){
            double value = this->engine->getOutputVariable(tag)->getValue();
            if (isnan(value)) {
                string message =  "ERROR: The value of fuzzy controller for " + tag + " is nun";
                cout<<message<<endl;
                throw invalid_fuzzy_output(message);
            }

            outputs.insert(std::pair<std::string,double>(tag,value));
        }
        return outputs;
    };
    void initialize(string controller_name){
        /* define the engine */
        this->engine = new Engine;
        this->engine->setName(controller_name);
        this->engine->setDescription("");
        /* define the controller */
        this->controller = new RuleBlock;
        this->controller->setName("mamdani");
        this->controller->setDescription("");
        this->controller->setEnabled(true);
        this->controller->setConjunction(new AlgebraicProduct);
        this->controller->setDisjunction(new AlgebraicSum);
        this->controller->setImplication(new Minimum);
        this->controller->setActivation(new General);
    }

    virtual void define_antecedents()=0;
    virtual void define_rules()=0;
    Engine *engine;
    RuleBlock *controller;
    myMap params;
    myMap default_inputs;
    vector<std::string> input_tags;
    vector<std::string> output_tags;
    
};
struct Fuzzy_TNFa:public base_model {
    Fuzzy_TNFa(myMap &params_):base_model(params_){
        this->initialize("Fuzzy_TNFa");
        this->define_antecedents();
        this->define_consequents();
        this->define_rules();
        this->reset();
    };
    void reset(){
        this->default_inputs["TNFa"] = 0;
        this->engine->restart();
    }

    void define_antecedents(){
        #// define antecedents
        vector<float> intervals = {0,1,10,100};
        InputVariable *input = new InputVariable;
        input->setName("TNFa");
        input->setDescription("");
        input->setEnabled(true);
        input->setRange(0, 100);
        input->setLockValueInRange(false);

        input->addTerm(new Triangle("Neg", intervals[0], intervals[0],intervals[1]));
        input->addTerm(new Triangle("Stim", intervals[0], intervals[1], intervals[2]));
        input->addTerm(new Triangle("High", intervals[1], intervals[2], intervals[3]));
        input->addTerm(new Triangle("Inhib", intervals[2], intervals[3], intervals[3]));

        this->engine->addInputVariable(input);
        
        this->input_tags.push_back("TNFa");
    }
    void define_rules(){
        vector<string> early_diff_rules = {
            "if TNFa is Stim then early_diff is H",
            "if (TNFa is Neg) or (TNFa is High) then early_diff is M",
            "if TNFa is Inhib then early_diff is L"
        };
        vector<string> late_diff_rules = {
            "if TNFa is Stim then late_diff is H",
            "if (TNFa is Neg) or (TNFa is High) then late_diff is M",
            "if TNFa is Inhib then late_diff is L"
        };
        for (auto&rule:early_diff_rules){
            this->controller->addRule(Rule::parse(rule.c_str(), this->engine));
        }
        for (auto&rule:late_diff_rules){
            this->controller->addRule(Rule::parse(rule.c_str(), this->engine));
        }
        this->engine->addRuleBlock(this->controller);
    }
};
struct Fuzzy_IL10:public base_model {
    Fuzzy_IL10(myMap &params_,bool above_48h):base_model(params_){
        this->initialize("Fuzzy_IL10");
        this->define_antecedents(above_48h);
        this->define_consequents();
        this->define_rules();
        this->reset();
    };
    void define_antecedents(){
        cout<<"ERROR: define_antecedents cannot be called on IL10 without argument"<<endl;
        throw invalid_fuzzy_definition("define_antecedents cannot be called on IL10 without argument");
    }
    void reset(){
        this->default_inputs["IL10"] = 0;
        this->engine->restart();
    }

    void define_antecedents(bool above_48h){
        #// define antecedents
        InputVariable *input = new InputVariable;
        input->setName("IL10");
        input->setDescription("");
        input->setEnabled(true);
        input->setRange(0, 100);
        input->setLockValueInRange(false);
        if (above_48h){
            vector<float> intervals = {0,0.1,1,10,100};
            input->addTerm(new Triangle("Neg", intervals[0], intervals[0],intervals[1]));
            input->addTerm(new Triangle("LowStim", intervals[0], intervals[1], intervals[2]));
            input->addTerm(new Triangle("HighStim", intervals[1], intervals[2], intervals[3]));
            input->addTerm(new Trapezoid("Inhib", intervals[2], intervals[3], intervals[4],intervals[4]));

        }else{
            vector<float> intervals = {0,1,10,100};
            input->addTerm(new Triangle("Neg", intervals[0], intervals[0],intervals[1]));
            input->addTerm(new Triangle("LowStim", intervals[0], intervals[1], intervals[2]));
            input->addTerm(new Triangle("HighStim", intervals[1], intervals[2], intervals[3]));
            input->addTerm(new Triangle("Inhib", intervals[2], intervals[3], intervals[3]));
        }
        this->engine->addInputVariable(input);
        this->input_tags.push_back("IL10");
    }
    void define_rules(){
        vector<string> early_diff_rules = {
            "if IL10 is HighStim then early_diff is VH",
            "if IL10 is LowStim then early_diff is H",
            "if IL10 is Neg then early_diff is M",
            "if IL10 is Inhib then early_diff is L"
        };
        vector<string> late_diff_rules = {
            "if IL10 is HighStim then late_diff is VH",
            "if IL10 is LowStim then late_diff is H",
            "if IL10 is Neg then late_diff is M",
            "if IL10 is Inhib then late_diff is L"
        };
        for (auto&rule:early_diff_rules){
            this->controller->addRule(Rule::parse(rule.c_str(), this->engine));
        }
        for (auto&rule:late_diff_rules){
            this->controller->addRule(Rule::parse(rule.c_str(), this->engine));
        }
        this->engine->addRuleBlock(this->controller);
    }
};
struct Fuzzy_IL8_IL1b:public base_model {
    Fuzzy_IL8_IL1b(myMap &params_):base_model(params_){
        this->initialize("Fuzzy_IL8_IL1b");
        this->define_antecedents();
        this->define_consequents();
        this->define_rules();
        this->reset();
    };
    void reset(){
        this->default_inputs["IL8"] = 0;
        this->default_inputs["IL1b"] = 0;
        this->engine->restart();
    }

    void define_antecedents(){
        #// define antecedents
        auto IL8 = [&](){
            vector<float> intervals = {0,this->params["IL8_M"],100};
            InputVariable *input = new InputVariable;
            input->setName("IL8");
            input->setDescription("");
            input->setEnabled(true);
            input->setRange(0, 100);
            input->setLockValueInRange(false);

            input->addTerm(new Triangle("Neg", intervals[0], intervals[0],intervals[1]));
            input->addTerm(new Triangle("LowStim", intervals[0], intervals[1], intervals[2]));
            input->addTerm(new Triangle("HighStim", intervals[1], intervals[2], intervals[2]));
            this->engine->addInputVariable(input);
            this->input_tags.push_back("IL8");
        };
        IL8();
        auto IL1b = [&](){
            vector<float> intervals = {0,this->params["IL1b_S"],this->params["IL1b_H"],200};
            InputVariable *input = new InputVariable;
            input->setName("IL1b");
            input->setDescription("");
            input->setEnabled(true);
            input->setRange(0, 100);
            input->setLockValueInRange(false);

            input->addTerm(new Triangle("Neg", intervals[0], intervals[0],intervals[1]));
            input->addTerm(new Triangle("Stim", intervals[0], intervals[1], intervals[2]));
            input->addTerm(new Trapezoid("High", intervals[1], intervals[2], intervals[3],intervals[3]));
            this->engine->addInputVariable(input);
            this->input_tags.push_back("IL1b");
        };
        IL1b();
    }
    void define_rules(){
        vector<string> early_diff_rules = {
            // only IL8
            "if (IL1b is Neg) and (IL8 is HighStim) then early_diff is EH",
            "if (IL1b is Neg) and (IL8 is LowStim) then early_diff is VH",
            "if (IL1b is Neg) and (IL8 is Neg) then early_diff is M",
            // only IL1b
            "if (IL1b is Stim) and (IL8 is Neg) then early_diff is VH",
            "if (IL1b is High) and (IL8 is Neg) then early_diff is M",
            // combind
            "if (IL1b is not Neg) and (IL8 is not Neg) then early_diff is VH"
        };

        for (auto&rule:early_diff_rules){
            this->controller->addRule(Rule::parse(rule.c_str(), this->engine));
        }

        this->engine->addRuleBlock(this->controller);
    }
};
