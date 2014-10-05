#include <boost/asio.hpp>
#include <stdexcept>
#include <signal.h>
#include <fstream>

#include "spacesim/networking/sim_server.hpp"
#include "spacesim/sim/simulation.hpp"
#include "spacesim/sim/physics_module.hpp"
#include "utils/json.hpp"

bool kill_flag = false;

void signal_handler(int _signal)
{
    kill_flag = true;
}

int main()
{
    const std::string savepath = "data/sim.state";
    
    struct sigaction signalHandler;
    signalHandler.sa_handler = signal_handler;
    sigemptyset(&signalHandler.sa_mask);
    signalHandler.sa_flags = 0;
    
    sigaction(SIGINT, &signalHandler, nullptr);
    
    std::cout << "starting server" << std::endl;
    
    boost::asio::io_service io_service;
    spacesim::sim::Simulation simulation;
    spacesim::networking::SimServer server(io_service, simulation, 40000);
    
    std::unique_ptr<spacesim::sim::PhysicsModule> physics(new spacesim::sim::PhysicsModule());
    
    simulation.add(std::move(physics));
    
    //simulation.setRates(1, 1.0 / spacesim::sim::Simulation::DefaultRate); // one tick per sec at normal speed
    //simulation.setRates(spacesim::sim::Simulation::DefaultRate, 1E-9); // slow motion
    //simulation.setRates(300000, 1E3); // MEGA fast forward

    if(false)
    {
        simulation.load(savepath);
    }
    else
    {
        utils::json::Object planets;
        std::ifstream planetFile("data/planets.json");
        planetFile >> planets;
        
        for(const auto &planet : planets.fields())
        {
            spacesim::sim::PhysicalBody::UniquePtr entity(new spacesim::sim::PhysicalBody(planet));
            
            const auto &blob = planets[planet];
            
            auto pos = spacesim::sim::VectorFromJson(blob["pos"]);
            auto vel = spacesim::sim::VectorFromJson(blob["vel"]);
            auto radius = blob["radius"].asDouble();
            auto mass = blob["mass"].asDouble();
            
            std::cout << "loaded planet '" << planet << "' " << pos << ", " << vel << ", " << radius << ", " << mass << std::endl;
            
            entity->setPosition(pos);
            entity->setVelocity(vel);
            entity->setRadius(radius);
            entity->setMass(mass);
            
            if(entity->name() == "Sol")
            {
                entity->setFixed(true);
            }
            
            simulation.add(std::move(entity));
        }
    }

    while(!kill_flag)
    {
        io_service.poll();
        simulation.update();
    }

    simulation.save(savepath);
    
    std::cout << "\rstopping server" << std::endl;
    
    return 0;
}
