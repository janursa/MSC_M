#include <iostream>
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>
#include <pybind11/stl.h>
#include <fuzzy/fuzzy.h>
namespace py=pybind11;
// class PyCell: public Cell{
//     using Cell::Cell;
//     using input_output = std::map<string,double>;
//     input_output run_policy(input_output inputs) override {
//         PYBIND11_OVERLOAD(
//             input_output,
//             Cell,
//             run_policy,
//             inputs
//         );
//     }
//     void reward() override {
//         PYBIND11_OVERLOAD(
//             void,
//             Cell,
//             reward
//         );
//     }
//     void step() override {
//         PYBIND11_OVERLOAD(
//             void,
//             Cell,
//             step
//         );
//     }
// };


PYBIND11_MODULE(fuzzy_cpp, m) {
    py::class_<Fuzzy_TNFa>(m,"Fuzzy_TNFa",py::dynamic_attr())
        .def(py::init<myMap&>())
        .def("forward",&Fuzzy_TNFa::forward)
        .def("reset",&Fuzzy_TNFa::reset);
    py::class_<Fuzzy_IL10>(m,"Fuzzy_IL10",py::dynamic_attr())
        .def(py::init<myMap&,bool>())
        .def("forward",&Fuzzy_IL10::forward)
        .def("reset",&Fuzzy_IL10::reset);
    py::class_<Fuzzy_IL8_IL1b>(m,"Fuzzy_IL8_IL1b",py::dynamic_attr())
        .def(py::init<myMap&>())
        .def("forward",&Fuzzy_IL8_IL1b::forward)
        .def("reset",&Fuzzy_IL8_IL1b::reset);
        
    //     .def("empty_neighbor", &PATCH::empty_neighbor,"Return an empty patch around the patch",
    //         py::arg("quiet")=false)
    //     .def("find_neighbor_agents",&PATCH::find_neighbor_agents,"Returns a vector of agents in one patch neighborhood",
    //         py::arg("include_self")=true)
    //     .def("get_agents",&PATCH::get_agents)
    //     .def("add_agent",&PATCH::add_agent)
    //     .def("remove_agent",&PATCH::remove_agent)
    //     .def("remove_agents",&PATCH::remove_agents)
    //     .def("empty",&PATCH::empty)
    //     .def_readwrite("on_border",&PATCH::on_border)
    //     .def_readwrite("neighbors",&PATCH::neighbors)
    //     .def_readwrite("index",&PATCH::index)
    //     .def_readwrite("env",&PATCH::env)
    //     .def_readwrite("coords",&PATCH::coords);
    // return class_binds_obj;
    
	/** defaults **/
 //    bind_tools::expose_defaults<myEnv,Cell,myPatch>(m);
 //    /** Envs **/
	// auto myEnv_binds = bind_tools::expose_env<myEnv,Cell,myPatch, bind_tools::tramEnv<myEnv,Cell,myPatch>>(m,"myEnv");
 //    myEnv_binds.def("collect_from_patches",&myEnv::collect_from_patches);
 //    myEnv_binds.def("collect_from_agents", &myEnv::collect_from_agents);
 //    myEnv_binds.def("set_GFs", &myEnv::set_GFs);

 //    myEnv_binds.def("get_GFs", &myEnv::get_GFs);
 //    // myEnv_binds.def("set_settings",&myEnv::set_settings);
 //    myEnv_binds.def("set_params",&myEnv::set_params);
 //    myEnv_binds.def("set_settings", &myEnv::set_settings);
 //    myEnv_binds.def("construct_policy", &myEnv::construct_policy);
 //    myEnv_binds.def("get_tick", &myEnv::get_tick);
 //    myEnv_binds.def("set_tick", &myEnv::set_tick);
 //    myEnv_binds.def("increment_tick", &myEnv::increment_tick);
 //    myEnv_binds.def("setup_agents", &myEnv::setup_agents);
	// /** Agent **/
 //    auto Cell_binds = bind_tools::expose_agent<myEnv,Cell,myPatch,PyCell>(m,"Cell");
 //    Cell_binds.def(py::init<shared_ptr<myEnv>,
 //                    string,
 //                    std::map<string,double>,
 //                    std::map<string,double>>(),
 //                    "Initialize",py::arg("env"),py::arg("class_name"),
 //                    py::arg("params"),py::arg("initial_conditions")
 //                    );
 //    Cell_binds.def("mortality",&Cell::mortality);
 //    Cell_binds.def("alkalinity",&Cell::alkalinity);
 //    Cell_binds.def("adaptation",&Cell::adaptation);
 //    Cell_binds.def("proliferation",&Cell::proliferation);
 //    Cell_binds.def("migration",&Cell::migration);
 //    Cell_binds.def("collect_policy_inputs",&Cell::collect_policy_inputs);
 //    /** Patch **/
 //    auto myPatch_binds = bind_tools::expose_patch<myEnv,Cell,myPatch>(m,"myPatch");
 //    myPatch_binds.def(py::init<shared_ptr<myEnv>,
 //                    MESH_ITEM,
 //                    std::map<string,double>,
 //                    std::map<string,double>,
 //                    std::map<string, bool>>(),
 //                    "Initialize",py::arg("env"),py::arg("mesh"),
 //                    py::arg("params"),py::arg("initial_conditions"), py::arg("flags"));
 //    myPatch_binds.def("initialize",&myPatch::initialize);

}




