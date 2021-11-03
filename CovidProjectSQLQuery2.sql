/*

Covid 19 Data Exploration 
Skills used: Joins, CTE's, Temp Tables, Windows Functions, Aggregate Functions, Creating Views, Converting Data Types

*/

-- <<< Deaths Data Exploration >>>

select * 
from PortfolioProject..CovidDeaths
Where continent is not null 
order by 3,4


-- Select Data that we are going to be starting with

Select Location, date, total_cases, new_cases, total_deaths, population
From PortfolioProject..CovidDeaths
Where continent is not null 
order by 1,2


-- Looking at Total Cases Vs Total Deaths
-- Shows liklihood of dying if you get infected in your country	

Select location, date, total_cases, total_deaths, (total_deaths / total_cases)*100 AS DeathsPercentage
From PortfolioProject..CovidDeaths
Where location = 'Egypt'
Order By 1,2


-- Looking at Total Cases Vs Population
-- Shows what percentage of population got infected

Select location, date, total_cases, population, (total_cases / population)*100 AS PercentagePopulationInfected
From PortfolioProject..CovidDeaths
--Where location = 'Egypt'
Order By 1,2


-- Countries with Highest Infection Rate compared to Population

Select location, population, MAX(total_cases) AS HighestInfectionCount , MAX((total_cases / population))*100 AS PercentagePopulationInfected
From PortfolioProject..CovidDeaths
Where continent is not null 
Group by location, population
--having location = 'Egypt'
Order By 4 DESC


-- Showing the countries with highest death count

Select location, population, MAX(Cast(total_deaths AS int)) AS HighestDeathCount , MAX((total_deaths / population))*100 AS PercentagePopulationDied
From PortfolioProject..CovidDeaths
Where continent is not null
Group by location, population
--having location = 'Egypt'
Order By HighestDeathCount DESC


-- LET'S BREAK THINGS DOWN BY CONTINENT
-- Showing contintents with the highest death count

Select continent, MAX(Cast(total_deaths AS int)) AS HighestDeathCount , MAX((total_deaths / population))*100 AS PercentagePopulationDied
From PortfolioProject..CovidDeaths
Where continent is not null
Group by continent
Order By HighestDeathCount DESC



-- GLOBAL NUMBERS PER DAY

Select date, SUM(new_cases) AS TotalCases, SUM(cast(new_deaths AS int)) AS TotalDeaths, (SUM(cast(new_deaths AS int)) / SUM(new_cases))*100 AS PercentagePopulationInfected
From PortfolioProject..CovidDeaths
Where continent is not null
Group by date
Order By date


-- ALL NUMBERS TILL TODAY (1-NOV-2021)
Select SUM(new_cases) AS TotalCases, SUM(cast(new_deaths AS int)) AS TotalDeaths, (SUM(cast(new_deaths AS int)) / SUM(new_cases))*100 AS PercentagePopulationInfected
From PortfolioProject..CovidDeaths
Where continent is not null

-----------------------------------------------


-- <<< Vaccination Data Exploration >>>

select * 
from PortfolioProject..CovidVaccination
Where continent is not null 
order by 3,4


-- Loking at total Population Vs Vaccination
-- Shows Percentage of Population that has recieved at least one Covid Vaccine

Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
SUM(Convert(bigint, vac.new_vaccinations)) Over(Partition by dea.location order by dea.location, dea.date ) AS RollingPropleVaccinated
--, (RollingeoPeopleVaccinated/ dea.population)*100   <<< ERROR, LOOK THE NEXT TOW QUERIES) >>>
From PortfolioProject..CovidDeaths AS dea
join PortfolioProject.. CovidVaccination AS vac
	on dea.location = vac.location
	and dea.date = vac.date
Where dea.continent is not null
order by 2,3


-- Using CTE to perform Calculation on Partition By in previous query
With PopvsVac ( continent, location, date, population, new_vaccinations, RollingeoPeopleVaccinated)
As
(
Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
SUM(Convert(bigint, vac.new_vaccinations)) Over(Partition by dea.location order by dea.location, dea.date ) AS RollingPropleVaccinated
From PortfolioProject..CovidDeaths AS dea
join PortfolioProject.. CovidVaccination AS vac
	on dea.location = vac.location
	and dea.date = vac.date
Where dea.continent is not null
--order by 2,3
)
Select *, (RollingeoPeopleVaccinated / population)*100 AS PercentagePopulationVaccinated
From PopvsVac


-- Using Temp Table to perform Calculation on Partition By in previous query
DROP Table if exists #PercentPopulationVaccinated
Create Table #PercentPopulationVaccinated
(
Continent nvarchar(255),
Location nvarchar(255),
Date datetime,
Population numeric,
New_vaccinations numeric,
RollingPeopleVaccinated numeric
)

Insert into #PercentPopulationVaccinated
Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, SUM(CONVERT(bigint,vac.new_vaccinations)) OVER (Partition by dea.Location Order by dea.location, dea.Date) as RollingPeopleVaccinated
--, (RollingPeopleVaccinated/population)*100
From PortfolioProject..CovidDeaths dea
Join PortfolioProject..CovidVaccination vac
	On dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null 
order by 2,3

Select *, (RollingPeopleVaccinated/Population)*100 AS PercentagePopulationVaccinated
From #PercentPopulationVaccinated

--------------------------------------

-- Creating example view to store data for later visualizations

Create View NumbersPerDay as
Select date, SUM(new_cases) AS TotalCases, SUM(cast(new_deaths AS int)) AS TotalDeaths, (SUM(cast(new_deaths AS int)) / SUM(new_cases))*100 AS PercentagePopulationInfected
From PortfolioProject..CovidDeaths
Where continent is not null
Group by date