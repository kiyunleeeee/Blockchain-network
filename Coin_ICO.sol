// Description
// This code is written in Solidity.
// This program is for initial coin offering.
// This program should run after blockchain network is built and several nodes join the network.


// check version of complier
pragma solidity >=0.7.0 <0.9.0;

contract hadcoin_ico {

    // introduce the maximum number of Coin available for sale
    uint public max_coin = 1000000; // uint: unsigned integer



    // introduce the USD to Coin conversion rate
    uint public usd_to_coin = 1000;



    // introduce the total number of Coin that have been bought by the investors
    uint public total_coin_bought = 0;



    // map from the investor address to its equity in Coin and USD
    mapping(address => uint) equity_coin;
    mapping(address => uint) equity_usd;



    // check if on investor can buy Coin
    modifier can_buy_coin(uint usd_invested) {
        require (usd_invested * usd_to_coin + total_coin_bought <= max_coin);
        _; // this function works only condition works
    }



    // get the equity in Coin of an investor
    function equity_in_coin(address investor) external constant returns (uint) { //address: type, investor: variable
        return equity_coin[investor];
    }



    //get the equity in USD of an investor
    function equity_in_usd(address investor) external constant returns (uint) {
        return equity_usd[investor];
    }



    // buy Coin
    function buy_coin(address investor, uint usd_invested) external
    can_buy_coin(usd_invested) {
        uint coin_bought = usd_invested * usd_to_coin;
        equity_coin[investor] += coin_bought;
        equity_in_usd[investor] = equity_coin[investor]/1000;
        total_coin_bought += coin_bought;
    }



    // sell Coin
    function sell_coin(address investor, uint coin_sold) external {
        equity_coin[investor] -= coin_sold;
        equity_in_usd[investor] = equity_coin[investor]/1000;
        total_coin_bought -= coin_sold;
    }
}